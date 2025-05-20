import React, { useState, useEffect, useCallback, useRef } from "react";
import { AlertTriangle, Info, ChevronRight } from "lucide-react";
import EventTrack from "../shared/EventTrack";
import Container from "../Container";

// Enable debugging to help troubleshoot issues
const DEBUG = true;
const log = (...args) => {
  if (DEBUG) {
    console.log(`[WordMeaningCheck]`, ...args);
  }
};

const WordMeaningCheck = ({
  validatedWords = [],
  sessionId,
  prolificId,
  onComplete,
}) => {
  // State management
  const [currentIndex, setCurrentIndex] = useState(0);
  const [meanings, setMeanings] = useState({});
  const [uniqueWords, setUniqueWords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showIntro, setShowIntro] = useState(true);
  const [completionMessage, setCompletionMessage] = useState(null);
  const [attemptedRecovery, setAttemptedRecovery] = useState(false);

  // Refs for tracking
  const startTime = useRef(new Date());
  const wordStartTime = useRef(new Date());
  const isSubmitted = useRef(false);
  const textareaRef = useRef(null);
  const safetyTimeoutRef = useRef(null);
  const completionTimeoutRef = useRef(null);

  // Calculate word difficulty score based on length and uncommon letters
  const calculateWordDifficulty = (word) => {
    try {
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

      score = score * word.length;
      return score;
    } catch (error) {
      log("Error calculating word difficulty:", error);
      // Default difficulty if calculation fails
      return word.length * 2;
    }
  };

  // Safety function to ensure progression even in case of failure
  const forceCompletion = useCallback(() => {
    log("Force completion triggered");

    if (!isSubmitted.current) {
      isSubmitted.current = true;

      // Clear any pending timeouts
      if (safetyTimeoutRef.current) {
        clearTimeout(safetyTimeoutRef.current);
      }

      if (completionTimeoutRef.current) {
        clearTimeout(completionTimeoutRef.current);
      }

      // Ensure we move to the next step
      onComplete([]);
    }
  }, [onComplete]);

  // Set up a global safety timeout to prevent being stuck
  useEffect(() => {
    if (!loading && !error && uniqueWords.length > 0 && !isSubmitted.current) {
      // Global safety timeout - ensures study continues even if everything else fails
      const globalTimeout = setTimeout(() => {
        log("Global safety timeout triggered");
        if (!isSubmitted.current) {
          setError(
            "The page took too long to respond. Proceeding to the next step."
          );
          forceCompletion();
        }
      }, 150000); // 2.5 minutes max for this page

      return () => clearTimeout(globalTimeout);
    }
  }, [loading, error, uniqueWords.length, forceCompletion]);

  // Add transition screen when moving away from intro
  const [showTransition, setShowTransition] = useState(false);

  // Handle dismissing the intro screen with a transition
  const handleDismissIntro = useCallback(() => {
    setShowTransition(true);

    // Show transition screen briefly, then move to main content
    setTimeout(() => {
      setShowIntro(false);
      setShowTransition(false);
    }, 1500);
  }, []);

  // First, fetch game results to get complete anagram information
  useEffect(() => {
    const fetchGameResults = async () => {
      try {
        log("Fetching game results");
        const response = await fetch(
          `${
            import.meta.env.VITE_API_URL
          }/api/game-results?sessionId=${sessionId}&prolificId=${prolificId}`
        );

        if (!response.ok) {
          throw new Error(`Failed to fetch game results: ${response.status}`);
        }

        const data = await response.json();
        log("Game results fetched successfully", {
          anagramCount: data.anagramDetails?.length,
        });

        // Create a map of words to their anagrams
        const wordAnagramMap = new Map();

        if (data.anagramDetails && Array.isArray(data.anagramDetails)) {
          data.anagramDetails.forEach((detail) => {
            if (detail.words && Array.isArray(detail.words)) {
              detail.words.forEach((word) => {
                if (word.word) {
                  wordAnagramMap.set(word.word.toUpperCase(), detail.anagram);
                }
              });
            }
          });
        }

        // Check if validatedWords is empty or undefined
        if (!validatedWords || validatedWords.length === 0) {
          log("No validated words found, skipping to completion");
          handleNoWordsCompletion();
          return;
        }

        // Create unique words with anagram information and calculate difficulty
        // Filter to only include valid words (words with reward value)
        const uniqueWordsMap = new Map();

        validatedWords.forEach((word) => {
          if (!word.word) {
            log("Invalid word entry:", word);
            return;
          }

          const upperWord = word.word.toUpperCase();
          // Only include valid words (those with a reward value)
          if (!uniqueWordsMap.has(upperWord) && word.reward > 0) {
            uniqueWordsMap.set(upperWord, {
              word: word.word,
              length: word.length || word.word.length,
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

        log("Processed words array", {
          totalWords: wordsArray.length,
          difficulties: wordsArray.map((w) => w.difficulty),
        });

        // Selection logic with fallback
        let selectedWords;

        if (wordsArray.length <= 3) {
          // If 3 or fewer words, check them all
          selectedWords = wordsArray;
        } else {
          // Otherwise, just take the top 3 most difficult words
          selectedWords = wordsArray.slice(0, 3);
        }

        // Safety check: If selection logic fails, use fallback
        if (selectedWords.length === 0 && wordsArray.length > 0) {
          log("Word selection produced no results, using fallback");
          selectedWords = wordsArray.slice(0, Math.min(3, wordsArray.length));
        }

        log("Selected words for meaning check", {
          count: selectedWords.length,
          words: selectedWords.map((w) => w.word),
        });

        setUniqueWords(selectedWords);

        if (selectedWords.length === 0) {
          log("No words selected for meaning check, skipping to completion");
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
        log("Error fetching game results:", error);
        setError(
          "Failed to initialize word meanings. Proceeding to the next step."
        );

        // Set a recovery timeout
        setTimeout(() => {
          if (!isSubmitted.current && !attemptedRecovery) {
            setAttemptedRecovery(true);
            forceCompletion();
          }
        }, 5000);
      } finally {
        setLoading(false);
      }
    };

    fetchGameResults();
  }, [
    sessionId,
    prolificId,
    validatedWords,
    forceCompletion,
    attemptedRecovery,
  ]);

  // Focus the textarea whenever currentIndex changes or when intro is dismissed
  useEffect(() => {
    if (!showIntro && textareaRef.current) {
      setTimeout(() => {
        try {
          textareaRef.current.focus();
        } catch (error) {
          log("Error focusing textarea:", error);
        }
      }, 100);
    }
  }, [currentIndex, showIntro]);

  const handleNoWordsCompletion = useCallback(async () => {
    try {
      log("Handling no words completion");

      if (!sessionId || !prolificId) {
        log("Missing session ID or Prolific ID");
        throw new Error("Missing session ID or Prolific ID");
      }

      // Log the event first
      await logEvent("meaning_check_complete", {
        totalWords: 0,
        reason: "no_validated_words",
      });

      isSubmitted.current = true;
      onComplete([]);
    } catch (error) {
      log("Error handling no words completion:", error);
      setError("Failed to complete phase. Proceeding to the next step.");

      // Force completion despite errors
      setTimeout(() => {
        if (!isSubmitted.current) {
          forceCompletion();
        }
      }, 3000);
    }
  }, [sessionId, prolificId, onComplete, forceCompletion]);

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
        log("Event logging error:", error);
        // Non-critical error, continue without event logging
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
      log("Submitting word meanings", { count: meaningData.length });

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

      log("Meanings submitted successfully");

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
      log("Failed to submit meanings:", error);
      setError("Failed to submit meanings. Proceeding to the next step.");

      // Force completion despite errors
      setTimeout(() => {
        if (!isSubmitted.current) {
          forceCompletion();
        }
      }, 3000);
    }
  };

  const handleSubmit = async (meaning) => {
    try {
      log("handleSubmit called", {
        currentIndex,
        totalWords: uniqueWords.length,
      });

      const currentWord = uniqueWords[currentIndex];
      if (!currentWord) {
        log("No current word found, forcing completion");
        forceCompletion();
        return;
      }

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
        log("Moving to next word", { nextIndex: currentIndex + 1 });
        setCurrentIndex((prev) => prev + 1);
        wordStartTime.current = new Date();
      } else {
        // Prepare for completion
        log("Preparing for completion");
        setCompletionMessage("Thank you for providing these word meanings!");

        // Set up safety timeout to ensure progression
        safetyTimeoutRef.current = setTimeout(() => {
          log("Safety timeout triggered");
          if (!isSubmitted.current) {
            forceCompletion();
          }
        }, 10000); // 10 second safety net

        // Normal completion flow
        completionTimeoutRef.current = setTimeout(() => {
          try {
            log("Normal completion flow executing");
            isSubmitted.current = true;

            // Prepare meaning data for submission with validation
            const meaningData = uniqueWords.map((word) => ({
              word: word.word,
              providedMeaning: meanings[word.word] || meaning || "",
              anagramShown: word.anagramShown || "",
              difficulty: word.difficulty || 0,
              submittedAt: new Date().toISOString(),
            }));

            // Submit meanings
            submitMeanings(meaningData);

            // Clear safety timeout since normal flow succeeded
            if (safetyTimeoutRef.current) {
              clearTimeout(safetyTimeoutRef.current);
            }
          } catch (error) {
            log("Error in completion timeout:", error);
            // Force completion despite errors
            forceCompletion();
          }
        }, 2000);
      }
    } catch (error) {
      log("Top-level handleSubmit error:", error);
      // Critical failure - force completion
      forceCompletion();
    }
  };

  // Cleanup effect for timeouts
  useEffect(() => {
    return () => {
      if (safetyTimeoutRef.current) {
        clearTimeout(safetyTimeoutRef.current);
      }
      if (completionTimeoutRef.current) {
        clearTimeout(completionTimeoutRef.current);
      }
    };
  }, []);

  // Emergency recovery UI - shown if we detect a problematic state
  if (
    !loading &&
    !error &&
    (!uniqueWords.length || currentIndex >= uniqueWords.length) &&
    !completionMessage &&
    !showIntro
  ) {
    log("Rendering emergency recovery UI");
    return (
      <Container>
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
            <div className="space-y-6 text-center">
              <div className="bg-red-50 p-6 rounded-lg">
                <AlertTriangle className="h-8 w-8 text-red-500 mx-auto mb-2" />
                <h3 className="text-xl font-semibold text-red-700 mb-3">
                  Something went wrong
                </h3>
                <p className="text-gray-700 mb-4">
                  We encountered an issue displaying the word meanings section.
                </p>
                <button
                  onClick={forceCompletion}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
                            transition-colors duration-200"
                >
                  Continue to Next Step
                </button>
              </div>
            </div>
          </div>
        </div>
      </Container>
    );
  }

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
        <p className="text-red-600 mb-4">{error}</p>
        <button
          onClick={forceCompletion}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
                   transition-colors duration-200"
        >
          Continue to Next Step
        </button>
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

  if (showTransition) {
    return (
      <Container>
        <div className="space-y-6">
          <div className="bg-white p-8 rounded-xl shadow-md border border-gray-100 text-center">
            <div className="animate-pulse">
              <div className="flex flex-col items-center justify-center space-y-6">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-2" />
                <h3 className="text-xl font-medium text-gray-800">
                  Loading words...
                </h3>

                <div className="bg-blue-50 max-w-lg mx-auto border border-blue-100 p-4 rounded-lg">
                  <div className="flex items-start">
                    <AlertTriangle className="h-5 w-5 text-blue-500 flex-shrink-0 mt-0.5 mr-2" />
                    <div>
                      <p className="font-medium text-blue-800">
                        Important Reminder
                      </p>
                      <p className="text-blue-700 text-sm mt-1">
                        If the screen appears blank for a few moments, please
                        wait patiently. The system will automatically continue.{" "}
                        <strong>Do not close this window.</strong>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Container>
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
                  <h3 className="text-md  text-gray-600">
                    Thank you for creating words and completing the survey!
                  </h3>
                  <div className="flex">
                    <Info className="h-5 w-5 text-blue-600 flex-shrink-0 mt-7" />
                    <p className="text-blue-700 text-lg ml-2 mt-6">
                      {uniqueWords.length === 1
                        ? "On the next page, we'll show you a valid word you created. To help us understand your word-building process, please explain what meaning you had in mind when you formed this word."
                        : `On the next page, we'll show you some of the interesting words you created. To help us understand your word-building process, please explain what meaning you had in mind when you formed each word.`}
                    </p>
                  </div>
                  {/* <p className="text-sm text-gray-500 italic mt-2">
                    This helps us understand how different people approach the
                    word-building process!
                  </p> */}
                </div>
              </div>

              {/* Important Warning Message */}
              <div className="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-md mt-16 mb-16">
                <div className="flex items-start">
                  <AlertTriangle className="h-5 w-5 text-amber-500 flex-shrink-0 mt-0.5 mr-2" />
                  <div>
                    <p className="font-semibold text-amber-800">
                      Important: Please Read
                    </p>

                    <p className="text-amber-700 text-sm mt-1">
                      {/* As we continue to optimize this game-playing website, you
                      may occasionally experience a momentary pause in some
                      browsers. <br /> */}
                      If you encounter <strong>a blank screen</strong> while
                      submitting the meaning in the next page, please{" "}
                      <strong>do not close the window</strong>. The system will
                      automatically proceed to the next step within few seconds.
                    </p>
                  </div>
                </div>
              </div>

              <button
                onClick={handleDismissIntro}
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

                {/* Added safety button in case the automatic transition fails */}
                <button
                  onClick={forceCompletion}
                  className="mt-6 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 
                           transition-colors duration-200 opacity-0 hover:opacity-100 focus:opacity-100"
                  aria-label="Continue if stuck"
                >
                  Continue
                </button>
              </div>
            </div>
          </div>
        </div>
      </Container>
    );
  }

  const currentWord = uniqueWords[currentIndex];

  // Safety check to ensure currentWord exists
  if (!currentWord) {
    log("Current word not found, rendering recovery UI");
    return (
      <Container>
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
            <div className="space-y-6 text-center">
              <div className="bg-yellow-50 p-6 rounded-lg">
                <AlertTriangle className="h-8 w-8 text-yellow-500 mx-auto mb-2" />
                <h3 className="text-xl font-semibold text-yellow-700 mb-3">
                  We're having trouble displaying the next word
                </h3>
                <button
                  onClick={forceCompletion}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
                           transition-colors duration-200"
                >
                  Continue to Next Step
                </button>
              </div>
            </div>
          </div>
        </div>
      </Container>
    );
  }

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

            {/* Emergency skip button - hidden by default but accessible via tab or if there's a problem */}
            {/* <button
              onClick={forceCompletion}
              className="w-full mt-4 py-2 bg-gray-100 text-gray-400 rounded-lg font-medium transition-all duration-200 cursor-pointer opacity-0 hover:opacity-100 focus:opacity-100"
              aria-label="Skip if having problems"
              tabIndex={0}
            >
              Having trouble? Skip to next step
            </button> */}
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
