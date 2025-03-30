import React, { useState, useEffect, useCallback, useRef } from "react";
import { AlertTriangle, Info, ChevronRight } from "lucide-react";
import EventTrack from "../shared/EventTrack";
import Container from "../Container";

const WordMeaningCheck = ({
  validatedWords = [],
  sessionId,
  prolificId,
  onComplete,
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [meanings, setMeanings] = useState({});
  const [uniqueWords, setUniqueWords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showIntro, setShowIntro] = useState(true);

  const startTime = useRef(new Date());
  const wordStartTime = useRef(new Date());
  const isSubmitted = useRef(false);
  const textareaRef = useRef(null); // Add a ref for the textarea

  // First, fetch game results to get complete anagram information
  useEffect(() => {
    const fetchGameResults = async () => {
      try {
        const response = await fetch(
          `${
            import.meta.env.VITE_API_URL
          }/api/game-results?sessionId=${sessionId}&prolificId=${prolificId}`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch game results");
        }
        const data = await response.json();

        // Create a map of words to their anagrams
        const wordAnagramMap = new Map();
        data.anagramDetails.forEach((detail) => {
          detail.words.forEach((word) => {
            wordAnagramMap.set(word.word.toUpperCase(), detail.anagram);
          });
        });

        // Create unique words with anagram information
        const uniqueWordsMap = new Map();

        // Check if validatedWords is empty or undefined
        if (!validatedWords || validatedWords.length === 0) {
          // Handle the case with no validated words
          console.log("No validated words found, skipping to completion");
          handleNoWordsCompletion();
          return;
        }

        validatedWords.forEach((word) => {
          const upperWord = word.word.toUpperCase();
          if (!uniqueWordsMap.has(upperWord)) {
            uniqueWordsMap.set(upperWord, {
              word: word.word,
              length: word.length,
              reward: word.reward,
              anagramShown: wordAnagramMap.get(upperWord) || "",
            });
          }
        });

        const unique = Array.from(uniqueWordsMap.values());
        setUniqueWords(unique);

        if (unique.length === 0) {
          handleNoWordsCompletion();
        } else {
          logEvent("meaning_check_start", {
            totalUniqueWords: unique.length,
            words: unique.map((w) => ({
              word: w.word,
              anagramShown: w.anagramShown,
            })),
          });
        }
      } catch (error) {
        console.error("Error fetching game results:", error);
        setError("Failed to initialize word meanings");
      } finally {
        setLoading(false);
      }
    };

    fetchGameResults();
  }, [sessionId, prolificId, validatedWords]);

  // Focus the textarea whenever currentIndex changes or when intro is dismissed
  useEffect(() => {
    if (!showIntro && textareaRef.current) {
      setTimeout(() => {
        textareaRef.current.focus();
      }, 100);
    }
  }, [currentIndex, showIntro]);

  const handleNoWordsCompletion = async () => {
    try {
      if (!sessionId || !prolificId) {
        throw new Error("Missing session ID or Prolific ID");
      }

      // Log the event first
      await logEvent("meaning_check_complete", {
        totalWords: 0,
        reason: "no_validated_words",
      });

      onComplete([]);
    } catch (error) {
      console.error("Error handling no words completion:", error);
      setError("Failed to complete phase. Please try again.");
    }
  };

  const logEvent = useCallback(
    async (eventType, details = {}) => {
      if (!sessionId || !prolificId) return;

      try {
        const currentWord = uniqueWords[currentIndex];
        const eventBody = {
          sessionId,
          prolificId,
          phase: "meaning_check",
          eventType,
          details: {
            word: details.word || currentWord?.word,
            providedMeaning: details.providedMeaning,
            anagramShown: details.anagramShown || currentWord?.anagramShown,
            reason: details.reason,
          },
          timestamp: new Date().toISOString(),
        };

        await fetch(`${import.meta.env.VITE_API_URL}/api/game-events`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(eventBody),
        });
      } catch (error) {
        console.error("Event logging error:", error);
      }
    },
    [sessionId, prolificId, uniqueWords, currentIndex]
  );

  const handlePageLeave = useCallback(() => {
    if (!isSubmitted.current) {
      const currentWord = uniqueWords[currentIndex];
      logEvent("page_leave", {
        word: currentWord?.word,
        anagramShown: currentWord?.anagramShown,
      });
    }
  }, [logEvent, uniqueWords, currentIndex]);

  const handlePageReturn = useCallback(() => {
    if (!isSubmitted.current) {
      const currentWord = uniqueWords[currentIndex];
      logEvent("page_return", {
        word: currentWord?.word,
        anagramShown: currentWord?.anagramShown,
      });
    }
  }, [logEvent, uniqueWords, currentIndex]);

  const handleInactiveStart = useCallback(() => {
    console.log("handleInactiveStart called in WordMeaningCheck");
    if (!isSubmitted.current) {
      const currentWord = uniqueWords[currentIndex];
      logEvent("mouse_inactive_start", {
        word: currentWord?.word,
        anagramShown: currentWord?.anagramShown,
      });
    }
  }, [logEvent, uniqueWords, currentIndex]);

  const handleActiveReturn = useCallback(() => {
    console.log("activeStart called in WordMeaningCheck");
    if (!isSubmitted.current) {
      const currentWord = uniqueWords[currentIndex];
      logEvent("mouse_active", {
        word: currentWord?.word,
        anagramShown: currentWord?.anagramShown,
      });
    }
  }, [logEvent, uniqueWords, currentIndex]);

  const handleSubmit = async (meaning) => {
    const currentWord = uniqueWords[currentIndex];
    if (!currentWord) return;

    // Log the meaning submission event
    await logEvent("meaning_submission", {
      word: currentWord.word,
      anagramShown: currentWord.anagramShown,
      providedMeaning: meaning,
    });

    // Update meanings state
    setMeanings((prev) => ({
      ...prev,
      [currentWord.word]: meaning,
    }));

    if (currentIndex < uniqueWords.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      wordStartTime.current = new Date();
    } else {
      try {
        isSubmitted.current = true;

        // Prepare meaning data for submission
        const meaningData = uniqueWords.map((word) => ({
          word: word.word,
          providedMeaning: meanings[word.word] || meaning,
          anagramShown: word.anagramShown,
          submittedAt: new Date().toISOString(),
        }));

        // Validate that all required fields are present
        const missingFields = meaningData.filter(
          (item) => !item.word || !item.providedMeaning || !item.anagramShown
        );

        if (missingFields.length > 0) {
          console.error("Missing fields in words:", missingFields);
          throw new Error("Missing required fields in word meanings");
        }

        // Submit meanings
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/meanings/submit`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              sessionId,
              prolificId,
              wordMeanings: meaningData,
              completedAt: new Date().toISOString(),
            }),
          }
        );

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || "Failed to submit meanings");
        }

        // Log completion
        await logEvent("meaning_check_complete", {
          totalWords: uniqueWords.length,
          // words: meaningData.map(({ word, anagramShown }) => ({
          //   word,
          //   anagramShown,
          // })),
        });

        onComplete(meaningData);
      } catch (error) {
        console.error("Failed to submit meanings:", error);
        setError(
          error.message || "Failed to submit meanings. Please try again."
        );
        isSubmitted.current = false;
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center p-6 bg-red-50 rounded-lg">
        <AlertTriangle className="h-8 w-8 text-red-500 mx-auto mb-2" />
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!loading && uniqueWords.length === 0) {
    return (
      <div className="space-y-6">
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
          <div className="space-y-6">
            <div className="flex items-start gap-4 bg-blue-50 p-6 rounded-lg">
              <Info className="h-6 w-6 text-blue-600 flex-shrink-0 mt-1" />
              <div className="space-y-4">
                <p className="text-blue-700">
                  Thank you for participating in the word creation activity and
                  completing the survey!
                </p>
                <p className="text-blue-700">
                  Let's proceed to learn more about the study.
                </p>
              </div>
            </div>
            <button
              onClick={() => onComplete([])}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
            >
              Continue
              <ChevronRight className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (showIntro) {
    return (
      <Container>
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
            <div className="space-y-6">
              <div className="flex items-start gap-4  p-6 rounded-lg">
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold ">
                    Thank you for creating words and completing the survey!
                  </h3>
                  <div className="flex">
                    <Info className="h-5 w-5 text-blue-600 flex-shrink-0 mt-7" />
                    {/* <p className="ml-2">
                    <span className="font-semibold text-amber-600">
                      Some of the words you created were not found in our
                      dictionary.
                    </span>
                  </p> */}
                    <p className="text-blue-700 text-lg ml-2 mt-6">
                      To help us understand your word-building process, could
                      you explain what meaning you had in mind for each word you
                      created?
                    </p>
                  </div>
                </div>
              </div>

              <button
                onClick={() => setShowIntro(false)}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
              >
                Continue
                <ChevronRight className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </Container>
    );
  }

  const currentWord = uniqueWords[currentIndex];

  return (
    <Container>
      <div className="space-y-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <div className="mb-4 flex items-center justify-between text-sm text-gray-500">
            <span>
              Word {currentIndex + 1} of {uniqueWords.length}
            </span>
            <div className="w-32 h-1.5 bg-gray-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-500 transition-all duration-300"
                style={{
                  width: `${((currentIndex + 1) / uniqueWords.length) * 100}%`,
                }}
              />
            </div>
          </div>

          <div className="text-center mb-6">
            <h3 className="text-3xl font-bold text-blue-600">
              {currentWord.word}
            </h3>
          </div>

          <div className="space-y-4">
            <textarea
              ref={textareaRef} // Add the ref here
              className="w-full p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 
                     focus:border-blue-500 min-h-[120px] text-gray-700"
              value={meanings[currentWord.word] || ""}
              onChange={(e) =>
                setMeanings((prev) => ({
                  ...prev,
                  [currentWord.word]: e.target.value,
                }))
              }
              placeholder="What does this word mean to you?"
            />

            <button
              onClick={() => handleSubmit(meanings[currentWord.word])}
              disabled={!meanings[currentWord.word]?.trim()}
              className={`w-full py-3 px-6 rounded-lg font-medium transition-all duration-200 cursor-pointer
              ${
                meanings[currentWord.word]?.trim()
                  ? "bg-blue-600 hover:bg-blue-700 text-white"
                  : "bg-gray-100 text-gray-400 cursor-not-allowed"
              }`}
            >
              {currentIndex < uniqueWords.length - 1 ? "Next Word" : "Complete"}
            </button>
          </div>
        </div>

        <EventTrack
          onPageLeave={handlePageLeave}
          onPageReturn={handlePageReturn}
          onInactivityStart={handleInactiveStart}
          onActiveReturn={handleActiveReturn}
          enabled={!isSubmitted.current}
          inactivityTimeout={5000}
        />
      </div>
    </Container>
  );
};

export default WordMeaningCheck;
