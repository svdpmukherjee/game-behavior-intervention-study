import React, { useState, useEffect, useCallback, useRef } from "react";
import {
  CheckCircle,
  XCircle,
  ChevronRight,
  AlertTriangle,
} from "lucide-react";

const DebriefPage = ({ sessionId, prolificId, onComplete, onStateChange }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [studyConfig, setStudyConfig] = useState(null);
  const [currentStep, setCurrentStep] = useState("results");
  const [resourceUsage, setResourceUsage] = useState({
    words: new Set(),
    none: false,
    selectAll: false,
  });

  // Add this to track when the step changes
  const prevStepRef = useRef(currentStep);

  useEffect(() => {
    if (onStateChange) {
      onStateChange(currentStep);
    }

    // Add scroll behavior when currentStep changes
    if (prevStepRef.current !== currentStep) {
      window.scrollTo({ top: 0, behavior: "smooth" });
      prevStepRef.current = currentStep;
    }
  }, [currentStep, onStateChange]);

  // Fetch both results and study config
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [resultsRes, configRes] = await Promise.all([
          fetch(
            `${
              import.meta.env.VITE_API_URL
            }/api/game-results?sessionId=${sessionId}&prolificId=${prolificId}`
          ),
          fetch(`${import.meta.env.VITE_API_URL}/api/study-config`),
        ]);

        if (!resultsRes.ok || !configRes.ok) {
          throw new Error("Failed to fetch required data");
        }

        const [resultsData, configData] = await Promise.all([
          resultsRes.json(),
          configRes.json(),
        ]);

        setResults(resultsData);
        setStudyConfig(configData);

        // Check if there are no words at all (both valid and invalid)
        const hasNoWords =
          (!resultsData.validWords || resultsData.validWords.length === 0) &&
          (!resultsData.invalidWords || resultsData.invalidWords.length === 0);

        // If there are no words, skip directly to debrief step
        if (hasNoWords) {
          setCurrentStep("debrief");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [sessionId, prolificId]);

  const handleSetStep = (step) => {
    setCurrentStep(step);
  };

  const handleResourceUsageChange = useCallback(
    (word) => {
      if (word === "none") {
        setResourceUsage((prev) => ({
          words: new Set(),
          none: !prev.none,
          selectAll: false,
        }));
      } else if (word === "selectAll") {
        setResourceUsage((prev) => {
          const allWords = results.validWords.concat(
            results.invalidWords || []
          );
          const allWordTexts = allWords.map((w) => w.word);

          // If not all words are currently selected, select all of them
          // Otherwise, deselect all words
          if (!prev.selectAll) {
            return {
              words: new Set(allWordTexts),
              none: false,
              selectAll: true,
            };
          } else {
            return {
              words: new Set(),
              none: false,
              selectAll: false,
            };
          }
        });
      } else {
        setResourceUsage((prev) => {
          const newWords = new Set(prev.words);

          if (newWords.has(word)) {
            newWords.delete(word);
          } else {
            newWords.add(word);
          }

          // Check if all words are now selected
          const allWords = results.validWords.concat(
            results.invalidWords || []
          );
          const allWordTexts = allWords.map((w) => w.word);
          const allSelected = allWordTexts.every((w) => newWords.has(w));

          return {
            words: newWords,
            none: false,
            selectAll: allSelected,
          };
        });
      }
    },
    [results]
  );

  const handleCompletion = async () => {
    try {
      // If there are no words, just complete without sending any data
      if (
        !results ||
        ((!results.validWords || results.validWords.length === 0) &&
          (!results.invalidWords || results.invalidWords.length === 0))
      ) {
        onComplete();
        return;
      }

      const {
        validWords = [],
        invalidWords = [],
        anagramDetails = [],
      } = results;
      const allWords = [...validWords, ...invalidWords];

      if (allWords.length === 0) {
        onComplete();
        return;
      }

      const selectedWords = Array.from(resourceUsage.words);

      // Create array of word-anagram pairs for selected words
      const wordsWithAnagrams = selectedWords.map((selectedWord) => {
        const wordInfo = allWords.find((w) => w.word === selectedWord);
        const anagramMatch = anagramDetails?.find((detail) =>
          detail.words.some(
            (w) => w.word.toUpperCase() === selectedWord.toUpperCase()
          )
        );
        return {
          word: selectedWord,
          length: wordInfo?.length,
          isValid: wordInfo?.reward !== undefined,
          anagramShown: anagramMatch?.anagram || "unknown",
        };
      });

      const eventDetails = {
        usedExternalResources: !resourceUsage.none,
        wordsWithExternalHelp: wordsWithAnagrams,
      };

      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/game-events`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sessionId,
            prolificId,
            phase: "debrief",
            eventType: "confessed_external_help",
            details: eventDetails,
            timestamp: new Date().toISOString(),
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to log resource usage response");
      }

      onComplete();
    } catch (error) {
      console.error("Error logging resource usage:", error);
      setError("Failed to submit response. Please try again.");
    }
  };

  if (loading) {
    return (
      <div className="text-center p-4">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto" />
        <p className="text-gray-600 mt-2">Loading results...</p>
      </div>
    );
  }

  if (error || !results) {
    return (
      <div className="text-center p-4">
        <p className="text-red-600">Error loading results: {error}</p>
      </div>
    );
  }

  const { validWords = [], invalidWords = [], totalReward = 0 } = results;
  const allWords = [...validWords, ...(invalidWords || [])].sort((a, b) => {
    if (b.length !== a.length) return b.length - a.length;
    return a.word.localeCompare(b.word);
  });

  // Check if there are any words at all
  const hasWords = allWords.length > 0;

  // Step 1: Results Display
  if (currentStep === "results") {
    return (
      <div className="space-y-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            Your Results
          </h2>

          <div className="space-y-6">
            {/* Valid Words Section */}
            <div>
              <div className="flex items-center">
                <h3 className="font-semibold mr-3">Valid Words Created:</h3>
                <div className="flex flex-wrap gap-2">
                  {validWords.length > 0 ? (
                    validWords.map((word, idx) => (
                      <span
                        key={`valid-${word.word}-${idx}`}
                        className="inline-flex items-center px-3 py-1 bg-green-50 text-green-700 rounded-full"
                      >
                        <CheckCircle className="h-4 w-4 mr-1" />
                        {word.word} ({word.length} letters - {word.reward}{" "}
                        pence)
                      </span>
                    ))
                  ) : (
                    <span className="text-gray-500">
                      No valid words created
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Invalid Words Section */}
            {invalidWords?.length > 0 && (
              <div>
                <div className="flex items-center">
                  <h3 className="font-semibold mr-3">Invalid Words Created:</h3>
                  <div className="flex flex-wrap gap-2">
                    {invalidWords.map((word, idx) => (
                      <span
                        key={`invalid-${word.word}-${idx}`}
                        className="inline-flex items-center px-3 py-1 bg-red-50 text-red-700 rounded-full"
                      >
                        <XCircle className="h-4 w-4 mr-1" />
                        {word.word} ({word.length} letters)
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Summary Stats */}
            <div className="bg-blue-50 border border-blue-100 rounded-lg p-6">
              <h3 className="font-semibold text-blue-800 mb-3">Summary</h3>
              <div className="space-y-2 text-gray-700">
                <p>Total valid words: {validWords.length}</p>
                {invalidWords?.length > 0 && (
                  <p>Total invalid words: {invalidWords.length}</p>
                )}

                {/* Calculate the displayed reward */}
                <p className="text-xl font-bold mt-4">
                  Your earned reward:{" "}
                  {Math.min(
                    totalReward,
                    studyConfig.compensation.max_reward_per_anagram *
                      studyConfig.game_anagrams
                  )}{" "}
                  pence
                </p>

                {/* Conditional message if the reward exceeds (number of anagram * maximum reward per anagram) */}
                {totalReward >
                  studyConfig.compensation.max_reward_per_anagram *
                    studyConfig.game_anagrams && (
                  <p className="text-sm font-medium italic text-blue-700 mt-2">
                    Maximum of{" "}
                    {studyConfig.compensation.max_reward_per_anagram *
                      studyConfig.game_anagrams}{" "}
                    pence was set for this study
                  </p>
                )}
              </div>
            </div>

            <button
              onClick={() => handleSetStep("debrief")}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
            >
              Tell Me About The Study Objective
              <ChevronRight className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Step 2: Study Debrief and Reward Update
  if (currentStep === "debrief") {
    return (
      <div className="space-y-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            Let us reveal some important details about this study
          </h2>

          <div className="space-y-6">
            {/* Research Purpose & Methodology section */}
            <div className="bg-blue-50 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-3">
                What This Study Was Really About
              </h3>
              <p className="text-gray-700">
                This study looked at how people approach word creation
                challenges and whether they play by the rules when nobody is
                watching. We used several ways to understand how people
                approach:
              </p>
              <ul className="list-disc list-inside mt-3 mb-4 space-y-2 text-gray-700">
                <li>Tracking whether you switched away from the webpage</li>
                <li>Noticing when your mouse stopped moving</li>
                <li>Measuring how long you spent on each word</li>
                <li>Tracking the sequence in which you formed words</li>
                <li>Overall patterns in how you found words</li>
              </ul>
              {/* <p className="text-gray-700 mt-4">
                When we asked you to explain what your words meant, we were
                trying to understand if you came up with the words on your own
                or found them somewhere else. This helps us learn more about how
                people behave when solving problems online.
              </p> */}
              <p className="text-gray-700 mt-4">
                We keep all your information private. Your prolificid will be
                replaced with a code, and only researchers can see your answers.
                We only use this information for our study, just as we promised.
              </p>
            </div>

            {/* Compensation Details section */}
            <div className="bg-green-50 border border-green-100 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-green-800 mb-3">
                Your Reward
              </h3>
              <p className="text-gray-700 mb-4">
                To be fair to everyone, we decided to give all participants the
                same bonus amount. No matter how many words you found, you will
                get the full possible reward.
              </p>
              {/* <p className="text-xl font-bold text-green-700">
                Your final reward:{" "}
                {studyConfig?.compensation?.max_reward_per_anagram *
                  studyConfig?.game_anagrams}{" "}
                pence ({studyConfig?.compensation?.max_reward_per_anagram} pence
                × {studyConfig?.game_anagrams} word puzzles)
              </p> */}
              <p className="text-xl font-bold text-green-700">
                Your final reward:{" "}
                {studyConfig?.compensation?.max_reward_per_anagram *
                  studyConfig?.game_anagrams}{" "}
                pence
              </p>
              <p className="text-sm text-gray-700 mt-4">
                Thank you for helping with our research! Your participation is
                really valuable.
              </p>
            </div>

            <button
              onClick={() =>
                hasWords ? setCurrentStep("feedback") : handleCompletion()
              }
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
            >
              {hasWords ? (
                <>
                  Continue to Final Step
                  <ChevronRight className="h-5 w-5" />
                </>
              ) : (
                <>
                  Complete Study
                  <ChevronRight className="h-5 w-5" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (currentStep === "feedback" && hasWords) {
    return (
      <div className="space-y-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="space-y-6">
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
              <div className="flex items-start gap-3 mb-6 ">
                <AlertTriangle className="h-7 w-7 text-amber-500 " />
                <div className="space-y-2.5">
                  <h3 className="font-semibold text-gray-800 text-lg">
                    Final Question
                  </h3>
                  <p className="text-gray-700">
                    We noticed some discrepancies in your response patterns.{" "}
                    <br />
                    Did you use any external help (such as websites or mobile
                    apps) for finding words?
                  </p>
                  <br />
                  <p className="text-sm text-gray-500">
                    You can select multiple words where you used external help.
                    <strong className="text-gray-700">
                      This will not affect your compensation or final reward
                      amount
                    </strong>
                  </p>
                </div>
              </div>

              <div className="space-y-3">
                {/* Select All option (only shown if there are at least 2 words) */}
                {allWords.length >= 2 && (
                  <label className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-amber-50 transition-colors duration-200 bg-amber-50">
                    <input
                      type="checkbox"
                      checked={resourceUsage.selectAll}
                      onChange={() => handleResourceUsageChange("selectAll")}
                      disabled={resourceUsage.none}
                      className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
                    />
                    <span className="font-medium">Select All Words</span>
                  </label>
                )}

                {/* Map through all words (valid and invalid) */}
                {allWords.map((word) => (
                  <label
                    key={word.word}
                    className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-blue-50 transition-colors duration-200"
                  >
                    <input
                      type="checkbox"
                      checked={resourceUsage.words.has(word.word)}
                      onChange={() => handleResourceUsageChange(word.word)}
                      disabled={resourceUsage.none}
                      className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
                    />
                    <span className="flex items-center gap-2">
                      <span>{word.word}</span>
                    </span>
                  </label>
                ))}
                <label className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-blue-50 transition-colors duration-200">
                  <input
                    type="checkbox"
                    checked={resourceUsage.none}
                    onChange={() => handleResourceUsageChange("none")}
                    className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
                  />
                  <span>No! I did not use any external help</span>
                </label>
              </div>
            </div>

            <button
              onClick={handleCompletion}
              disabled={resourceUsage.words.size === 0 && !resourceUsage.none}
              className={`w-full py-3 rounded-lg font-medium transition-colors cursor-pointer ${
                resourceUsage.words.size === 0 && !resourceUsage.none
                  ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700 text-white"
              }`}
            >
              Continue to Completion
            </button>
            {resourceUsage.words.size === 0 && !resourceUsage.none && (
              <p className="text-red-400 text-sm text-center mt-2">
                Please select at least one checkbox to continue
              </p>
            )}
          </div>
        </div>
      </div>
    );
  }
};

export default DebriefPage;
