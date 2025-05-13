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
  const [completionMessage, setCompletionMessage] = useState(null);

  const startTime = useRef(new Date());
  const wordStartTime = useRef(new Date());
  const isSubmitted = useRef(false);
  const textareaRef = useRef(null);

  // Calculate word difficulty score based on length and uncommon letters
  const calculateWordDifficulty = (word) => {
    // Base score from word length (longer words are harder)
    let score = 0;

    // Add points for uncommon letters (JQXZ are most uncommon)
    const uncommonLetters = {
      q: 10,
      z: 10,
      x: 8,
      j: 8,
      v: 6,
      w: 6,
      y: 4,
      k: 5,
      f: 5,
      h: 4,
      b: 3,
      c: 3,
      g: 3,
      m: 3,
      p: 3,
      d: 2,
      l: 2,
      u: 2,
      n: 1,
      o: 1,
      r: 1,
      s: 1,
      t: 1,
      a: 1,
      e: 1,
      i: 1,
    };

    // Sum difficulty scores for each letter
    for (const letter of word.toLowerCase()) {
      score += uncommonLetters[letter] || 1;
    }

    // Add points for difficult letter combinations
    // const difficultCombinations = [
    //   "qu",
    //   "xh",
    //   "ph",
    //   "mn",
    //   "gh",
    //   "rh",
    //   "th",
    //   "ch",
    //   "sh",
    // ];
    // for (const combo of difficultCombinations) {
    //   if (word.toLowerCase().includes(combo)) {
    //     score += 5;
    //   }
    // }
    score = score * word.length;

    return score;
  };

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

        // Check if validatedWords is empty or undefined
        if (!validatedWords || validatedWords.length === 0) {
          console.log("No validated words found, skipping to completion");
          handleNoWordsCompletion();
          return;
        }

        // Create unique words with anagram information and calculate difficulty
        // Filter to only include valid words (words with reward value)
        const uniqueWordsMap = new Map();
        validatedWords.forEach((word) => {
          const upperWord = word.word.toUpperCase();
          // Only include valid words (those with a reward value)
          if (!uniqueWordsMap.has(upperWord) && word.reward > 0) {
            uniqueWordsMap.set(upperWord, {
              word: word.word,
              length: word.length,
              reward: word.reward,
              anagramShown: wordAnagramMap.get(upperWord) || "",
              difficulty: calculateWordDifficulty(word.word),
              isValid: true,
            });
          }
        });

        // Convert to array and sort by difficulty (highest first)
        const wordsArray = Array.from(uniqueWordsMap.values()).sort(
          (a, b) => b.difficulty - a.difficulty
        );

        // Selection logic:
        let selectedWords;
        if (wordsArray.length <= 3) {
          // If 3 or fewer words, check them all
          selectedWords = wordsArray;
        } else {
          // Otherwise, just take the top 3 most difficult words
          selectedWords = wordsArray.slice(0, 3);
        }

        setUniqueWords(selectedWords);

        if (selectedWords.length === 0) {
          handleNoWordsCompletion();
        } else {
          logEvent("meaning_check_start", {
            totalUniqueWords: selectedWords.length,
            totalValidWords: wordsArray.length,
            words: selectedWords.map((w) => ({
              word: w.word,
              anagramShown: w.anagramShown,
              difficulty: w.difficulty,
              isValid: true, // All selected words are valid
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
            difficulty: details.difficulty || currentWord?.difficulty,
            reason: details.reason,
            totalWords: details.totalWords,
            totalValidWords: details.totalValidWords,
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
        difficulty: currentWord?.difficulty,
      });
    }
  }, [logEvent, uniqueWords, currentIndex]);

  const handlePageReturn = useCallback(() => {
    if (!isSubmitted.current) {
      const currentWord = uniqueWords[currentIndex];
      logEvent("page_return", {
        word: currentWord?.word,
        anagramShown: currentWord?.anagramShown,
        difficulty: currentWord?.difficulty,
      });
    }
  }, [logEvent, uniqueWords, currentIndex]);

  const handleInactiveStart = useCallback(() => {
    if (!isSubmitted.current) {
      const currentWord = uniqueWords[currentIndex];
      logEvent("mouse_inactive_start", {
        word: currentWord?.word,
        anagramShown: currentWord?.anagramShown,
        difficulty: currentWord?.difficulty,
      });
    }
  }, [logEvent, uniqueWords, currentIndex]);

  const handleActiveReturn = useCallback(() => {
    if (!isSubmitted.current) {
      const currentWord = uniqueWords[currentIndex];
      logEvent("mouse_active", {
        word: currentWord?.word,
        anagramShown: currentWord?.anagramShown,
        difficulty: currentWord?.difficulty,
      });
    }
  }, [logEvent, uniqueWords, currentIndex]);

  const submitMeanings = async (meaningData) => {
    try {
      // Submit meanings to backend
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
        words: meaningData.map(({ word, anagramShown, difficulty }) => ({
          word,
          anagramShown,
          difficulty,
        })),
      });

      // Complete the phase
      onComplete(meaningData);
    } catch (error) {
      console.error("Failed to submit meanings:", error);
      setError(error.message || "Failed to submit meanings. Please try again.");
      isSubmitted.current = false;
    }
  };

  const handleSubmit = async (meaning) => {
    const currentWord = uniqueWords[currentIndex];
    if (!currentWord) return;

    // Log the meaning submission event
    await logEvent("meaning_submission", {
      word: currentWord.word,
      anagramShown: currentWord.anagramShown,
      providedMeaning: meaning,
      difficulty: currentWord.difficulty,
    });

    // Update meanings state
    setMeanings((prev) => ({
      ...prev,
      [currentWord.word]: meaning,
    }));

    if (currentIndex < uniqueWords.length - 1) {
      // Move to next word
      setCurrentIndex((prev) => prev + 1);
      wordStartTime.current = new Date();
    } else {
      // Prepare for completion
      setCompletionMessage("Thank you for providing these word meanings!");

      // Slight delay before completing
      setTimeout(() => {
        try {
          isSubmitted.current = true;

          // Prepare meaning data for submission
          const meaningData = uniqueWords.map((word) => ({
            word: word.word,
            providedMeaning: meanings[word.word] || meaning,
            anagramShown: word.anagramShown,
            difficulty: word.difficulty,
            submittedAt: new Date().toISOString(),
          }));

          // Submit meanings
          submitMeanings(meaningData);
        } catch (error) {
          console.error("Failed to submit meanings:", error);
          setError(
            error.message || "Failed to submit meanings. Please try again."
          );
          isSubmitted.current = false;
        }
      }, 1000);
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
              <div className="flex items-start gap-4 p-6 rounded-lg">
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold">
                    Thank you for creating words and completing the survey!
                  </h3>
                  <div className="flex">
                    <Info className="h-5 w-5 text-blue-600 flex-shrink-0 mt-7" />
                    <p className="text-blue-700 text-lg ml-2 mt-6">
                      {uniqueWords.length === 1
                        ? "To help us understand your word-building process, could you explain what meaning you had in mind for this valid word you created?"
                        : `To help us understand your word-building process, we have selected some of your interesting words. Could you tell us what meaning you had in mind for each?`}
                      {/* {uniqueWords.length === 1
                        ? "To help us understand your word-building process, could you explain what meaning you had in mind for this valid word you created?"
                        : `To help us understand your word-building process, we've selected ${
                            uniqueWords.length
                          } of your ${
                            uniqueWords.length ===
                            validatedWords.filter((w) => w.reward > 0).length
                              ? ""
                              : "most interesting"
                          } valid words. Could you tell us what meaning you had in mind for each?`} */}
                    </p>
                  </div>
                  <p className="text-sm text-gray-500 italic mt-2">
                    This helps us understand how different people approach the
                    word-building process!
                  </p>
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

  if (completionMessage) {
    return (
      <Container>
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
            <div className="space-y-6 text-center">
              <div className="bg-green-50 p-6 rounded-lg">
                <div className="flex items-center justify-center space-x-2 mb-4">
                  <svg
                    className="h-6 w-6 text-green-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <h3 className="text-xl font-semibold text-green-700">
                    {completionMessage}
                  </h3>
                </div>
                <p className="text-green-600">Processing your responses...</p>
              </div>
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
            {/* Optional: Show word length for context */}
            <p className="text-sm text-gray-500 mt-1">
              ({currentWord.length} letters)
            </p>
          </div>

          <div className="space-y-4">
            <textarea
              ref={textareaRef}
              className="w-full p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 
                     focus:border-blue-500 min-h-[120px] text-gray-700"
              value={meanings[currentWord.word] || ""}
              onChange={(e) =>
                setMeanings((prev) => ({
                  ...prev,
                  [currentWord.word]: e.target.value,
                }))
              }
              placeholder="What does this word mean to you? How would you use it in a sentence?"
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
