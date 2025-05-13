import { useState, useEffect, useCallback, useRef } from "react";
import GameBoard from "./GameBoard";
import {
  AlertTriangle,
  Timer,
  Award,
  Info,
  CheckCircle,
  XCircle,
} from "lucide-react";
import EventTrack from "../shared/EventTrack";
import game_gif from "../../assets/game_play.gif";
import Container from "../Container";

const TutorialGame = ({ prolificId, sessionId, onComplete }) => {
  // State management
  const [gameState, setGameState] = useState({
    tutorialWord: "",
    solution: [],
    availableLetters: [],
    validatedWords: [],
    timeLeft: 0,
    totalTime: 0,
    isTimeUp: false,
    solutions: {},
  });
  const [studyConfig, setStudyConfig] = useState(null);
  const [notification, setNotification] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showOverview, setShowOverview] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [submissionResults, setSubmissionResults] = useState(null);
  const [skillLevel, setSkillLevel] = useState(5);
  const [isSubmittingSkill, setIsSubmittingSkill] = useState(false);

  // Refs
  const timerRef = useRef(null);
  const isSubmitted = useRef(false);
  const videoRef = useRef(null);
  const startTime = useRef(new Date());

  // Add refs for alert handling and visibility tracking
  const timeUpAlertShown = useRef(false);
  const pendingSubmission = useRef(false);
  const visibilityChangeHandled = useRef(false);

  // Show notification helper
  const showNotification = useCallback((message, isError = false) => {
    setNotification({ message, isError });
    setTimeout(() => setNotification(null), 3000);
  }, []);

  // Calculate reward based on word length
  const calculateReward = useCallback(
    (wordLength, isValid) => {
      if (!studyConfig?.rewards || !isValid) return 0;
      return studyConfig.rewards[wordLength.toString()] || 0;
    },
    [studyConfig]
  );

  // Log game events
  const logGameEvent = useCallback(
    async (eventType, details = null) => {
      try {
        await fetch(`${import.meta.env.VITE_API_URL}/api/game-events`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sessionId,
            prolificId,
            phase: "tutorial",
            anagramShown: gameState.tutorialWord,
            eventType,
            details: {
              ...details,
            },
            timestamp: new Date().toISOString(),
          }),
        });
      } catch (error) {
        console.error("Event logging error:", error);
      }
    },
    [sessionId, prolificId, gameState.tutorialWord]
  );

  // Event tracking handlers
  const handleInactiveStart = useCallback(() => {
    if (!showOverview && !isSubmitted.current) {
      logGameEvent("mouse_inactive_start");
    }
  }, [showOverview, logGameEvent]);

  const handleActiveReturn = useCallback(() => {
    if (!showOverview && !isSubmitted.current) {
      logGameEvent("mouse_active");
    }
  }, [showOverview, logGameEvent]);

  const handlePageLeave = useCallback(() => {
    if (!showOverview && !isSubmitted.current) {
      logGameEvent("page_leave");
    }
  }, [showOverview, logGameEvent]);

  const handlePageReturn = useCallback(() => {
    if (!showOverview && !isSubmitted.current) {
      logGameEvent("page_return");
    }
  }, [showOverview, logGameEvent]);

  // Initialize tutorial
  const initTutorial = useCallback(async () => {
    try {
      const [configResponse, tutorialResponse] = await Promise.all([
        fetch(`${import.meta.env.VITE_API_URL}/api/study-config`),
        fetch(
          `${
            import.meta.env.VITE_API_URL
          }/api/tutorial/init?sessionId=${sessionId}`
        ),
      ]);

      const [configData, tutorialData] = await Promise.all([
        configResponse.json(),
        tutorialResponse.json(),
      ]);

      if (!configResponse.ok || !tutorialResponse.ok) {
        throw new Error("Failed to initialize tutorial");
      }

      setStudyConfig(configData);
      setGameState((prev) => ({
        ...prev,
        tutorialWord: tutorialData.word,
        solutions: tutorialData.solutions,
        availableLetters: tutorialData.word.split(""),
        timeLeft: configData.timeSettings.tutorial_time,
        totalTime: configData.timeSettings.tutorial_time,
      }));
    } catch (error) {
      setError(error.message);
      showNotification("Failed to initialize tutorial", true);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, showNotification]);

  // Check if a word is valid
  const isValidWord = useCallback(
    (word) => {
      if (!word || !gameState.solutions) return false;
      const wordLength = word.length.toString();
      const solutionsForLength = gameState.solutions[wordLength];
      return solutionsForLength?.includes(word.toUpperCase());
    },
    [gameState.solutions]
  );

  // Handle word validation
  const handleValidate = useCallback(() => {
    const word = gameState.solution.join("");

    if (gameState.validatedWords.some((w) => w.word === word)) {
      showNotification("This word has already been recorded", true);
      return;
    }

    const valid = isValidWord(word);
    logGameEvent("word_validation", {
      word,
      wordLength: word.length,
      isValid: valid,
    });

    setGameState((prev) => ({
      ...prev,
      validatedWords: [
        ...prev.validatedWords,
        { word, length: word.length, validatedAt: new Date().toISOString() },
      ],
      solution: [],
      availableLetters: prev.tutorialWord.split(""),
    }));

    showNotification("Word has been recorded");
  }, [
    gameState.solution,
    gameState.tutorialWord,
    gameState.validatedWords,
    logGameEvent,
    showNotification,
    isValidWord,
  ]);

  // Handle word removal
  const handleRemoveWord = useCallback(
    async (index) => {
      const removedWord = gameState.validatedWords[index];
      if (!removedWord) return;

      await logGameEvent("word_removal", {
        word: removedWord.word,
        wordLength: removedWord.length,
        timeInList: Date.now() - new Date(removedWord.validatedAt).getTime(),
      });

      setGameState((prev) => ({
        ...prev,
        validatedWords: prev.validatedWords.filter((_, i) => i !== index),
      }));

      showNotification(`Removed word: ${removedWord.word}`);
    },
    [gameState.validatedWords, logGameEvent, showNotification]
  );

  // Handle submission of words
  const handleSubmit = useCallback(async () => {
    if (isSubmitting || isSubmitted.current) return;

    try {
      setIsSubmitting(true);
      isSubmitted.current = true;

      const currentTimeSpent = Date.now() - startTime.current.getTime();

      // Process words and calculate rewards
      const processedWords = gameState.validatedWords.map((word) => ({
        word: word.word,
        length: word.length,
        reward: calculateReward(word.length, isValidWord(word.word)),
        isValid: isValidWord(word.word),
      }));

      const validWords = processedWords.filter((word) => word.isValid);
      const invalidWords = processedWords.filter((word) => !word.isValid);
      const totalReward = validWords.reduce(
        (sum, word) => sum + (word.reward || 0),
        0
      );

      setSubmissionResults({
        validWords,
        invalidWords,
        totalReward,
      });

      await logGameEvent("word_submission", {
        words: processedWords,
        isTimeUp: gameState.isTimeUp,
        timeSpent: currentTimeSpent,
      });

      setShowResults(true);
    } catch (error) {
      console.error("Tutorial submission error:", error);
      setNotification({
        message: "Failed to submit tutorial results. Please try again.",
        isError: true,
      });
      setIsSubmitting(false);
      isSubmitted.current = false;
    } finally {
      setIsSubmitting(false);
    }
  }, [
    gameState.validatedWords,
    gameState.isTimeUp,
    calculateReward,
    isValidWord,
    logGameEvent,
    isSubmitting,
  ]);

  // Handle completion of practice
  const handleCompletePractice = async () => {
    try {
      // Update tutorial completion status in backend
      await fetch(`${import.meta.env.VITE_API_URL}/api/tutorial/complete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId,
          prolificId,
          completedAt: new Date().toISOString(),
          validatedWords: gameState.validatedWords,
        }),
      });

      // Proceed to next phase
      onComplete();
    } catch (error) {
      console.error("Error completing tutorial:", error);
      setNotification({
        message: "Failed to complete practice round. Please try again.",
        isError: true,
      });
    }
  };

  const logSkillLevel = async (skillLevel) => {
    try {
      setIsSubmittingSkill(true);

      // Create the event body
      const eventBody = {
        sessionId,
        prolificId,
        phase: "tutorial",
        eventType: "self_reported_skill",
        details: {
          skillLevel: skillLevel,
        },
        timestamp: new Date().toISOString(),
      };

      // Post to the game-events endpoint
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/game-events`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(eventBody),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to log skill level");
      }

      // After successful submission, hide the overview and start the game
      setShowOverview(false);
    } catch (error) {
      console.error("Error logging skill level:", error);
      // Even if there's an error, still allow the user to proceed
      setShowOverview(false);
    } finally {
      setIsSubmittingSkill(false);
    }
  };

  // Timer effect
  useEffect(() => {
    if (!showOverview && gameState.timeLeft > 0 && !isSubmitted.current) {
      timerRef.current = setInterval(() => {
        setGameState((prev) => {
          if (prev.timeLeft <= 1) {
            clearInterval(timerRef.current);

            // Set isTimeUp first
            const newState = { ...prev, timeLeft: 0, isTimeUp: true };

            // Only show alert if document is visible and it hasn't been shown yet
            if (
              document.visibilityState === "visible" &&
              !timeUpAlertShown.current
            ) {
              timeUpAlertShown.current = true;
              // Use setTimeout to ensure state is updated before alert
              setTimeout(() => {
                if (!isSubmitted.current) {
                  alert(
                    "Time's up! All of your added words have been submitted. Let's review your practice round results"
                  );
                  handleSubmit();
                }
              }, 50);
            } else if (!timeUpAlertShown.current) {
              // If document is not visible, mark as pending
              pendingSubmission.current = true;
            }

            return newState;
          }
          return { ...prev, timeLeft: prev.timeLeft - 1 };
        });
      }, 1000);

      return () => {
        if (timerRef.current) {
          clearInterval(timerRef.current);
        }
      };
    }
  }, [gameState.timeLeft, showOverview, handleSubmit]);

  // Handle page visibility change
  useEffect(() => {
    function handleVisibilityChange() {
      // Check if we need to show the alert when user returns to page
      if (
        document.visibilityState === "visible" &&
        pendingSubmission.current &&
        !isSubmitted.current &&
        !timeUpAlertShown.current &&
        gameState.isTimeUp
      ) {
        timeUpAlertShown.current = true;
        pendingSubmission.current = false;
        visibilityChangeHandled.current = true;

        // Add a slight delay to ensure DOM is ready
        setTimeout(() => {
          if (!isSubmitted.current) {
            alert(
              "Time's up! All of your added words have been submitted. Let's review your practice round results"
            );
            handleSubmit();
          }
        }, 100);
      }
    }

    document.addEventListener("visibilitychange", handleVisibilityChange);
    return () =>
      document.removeEventListener("visibilitychange", handleVisibilityChange);
  }, [gameState.isTimeUp, handleSubmit]);

  // Additional effect to catch any missed time-up alerts - NEW
  useEffect(() => {
    if (
      gameState.isTimeUp &&
      !isSubmitted.current &&
      !timeUpAlertShown.current &&
      !pendingSubmission.current &&
      !visibilityChangeHandled.current &&
      document.visibilityState === "visible"
    ) {
      timeUpAlertShown.current = true;

      // Add a slight delay to ensure DOM is ready
      setTimeout(() => {
        if (!isSubmitted.current) {
          alert(
            "Time's up! All of your added words have been submitted. Let's review your practice round results"
          );
          handleSubmit();
        }
      }, 100);
    }
  }, [gameState.isTimeUp, handleSubmit]);

  // Reset timer when user starts the game
  useEffect(() => {
    if (!showOverview) {
      startTime.current = new Date();
      // Reset alert flags when starting the game
      timeUpAlertShown.current = false;
      pendingSubmission.current = false;
      visibilityChangeHandled.current = false;
    }
  }, [showOverview]);

  // Initialize tutorial when sessionId is available
  useEffect(() => {
    if (sessionId) {
      initTutorial();
    }
  }, [sessionId, initTutorial]);

  // Loading state
  if (isLoading) {
    return (
      <div className="flex justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="text-center p-6">
        <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <p className="text-red-600 mb-4">{error}</p>
      </div>
    );
  }

  // Results view
  if (showResults && submissionResults) {
    const { validWords, invalidWords, totalReward } = submissionResults;

    return (
      <Container>
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Practice Round Results
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
                    <h3 className="font-semibold mr-3">
                      Invalid Words Created:
                    </h3>
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
              <div className="bg-blue-50 border border-blue-100 rounded-lg p-6 ">
                <h3 className="font-semibold text-blue-800 mb-3">Summary</h3>
                <div className="space-y-2 text-gray-700">
                  <p>Total valid words: {validWords.length}</p>
                  {invalidWords?.length > 0 && (
                    <p>Total invalid words: {invalidWords.length}</p>
                  )}
                  <p className="text-xl font-bold mt-4">
                    Practice round reward: {Math.min(totalReward, 30)} pence
                  </p>
                  {/* Conditional message if the reward exceeds maximum */}
                  {totalReward > 30 && (
                    <p className="text-sm font-medium text-blue-700 mt-2">
                      Maximum of 30p is assigned per word solving
                    </p>
                  )}
                </div>

                {/* Motivation Message */}
                <div className="mt-6 p-4 bg-white rounded-lg">
                  <p className="text-green-800 ">
                    {totalReward > 0 ? (
                      <>
                        Great job! You are doing well with word creation. Keep
                        this up in the main game!
                        <br />
                        <br />
                        <span className=" text-red-500">
                          This reward is for display only. Rewards will be
                          distributed based on the main game performance.
                        </span>
                      </>
                    ) : (
                      "Great job! You're doing well with word creation. This was just a practice."
                    )}
                  </p>
                </div>
              </div>

              <button
                onClick={handleCompletePractice}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-colors cursor-pointer"
              >
                Complete Practice Round
              </button>
            </div>
          </div>
        </div>
      </Container>
    );
  }

  // Tutorial overview screen
  if (showOverview && studyConfig) {
    const rewards = studyConfig.rewards;
    const minLength = Math.min(...Object.keys(rewards).map(Number));
    const maxLength = Math.max(...Object.keys(rewards).map(Number));
    const tutorialTime = studyConfig.timeSettings.tutorial_time / 60;

    return (
      <Container>
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-white to-blue-50 p-8 rounded-3xl shadow-lg border-2 border-gray-300 space-y-6">
            <div className="flex items-center gap-3 mb-4">
              <Info className="h-6 w-6 text-blue-600" />
              <h3 className="text-2xl font-extrabold text-gray-800">
                How To Play
              </h3>
            </div>

            <div className="space-y-4">
              <div className="bg-white p-6 rounded-lg">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
                  <div className="order-2 md:order-1 m-auto">
                    <ul className="space-y-1 text-blue-700">
                      <li className="hover:bg-blue-100 p-2 rounded-lg">
                        • Drag and drop letters{" "}
                        <span className="font-semibold text-amber-600">
                          using mouse
                        </span>{" "}
                        to form valid English words
                      </li>
                      <li className="hover:bg-blue-100 p-2 rounded-lg">
                        • Each word must contain at least {minLength} letters
                      </li>
                      <li className="hover:bg-blue-100 p-2 rounded-lg">
                        • Click{" "}
                        <span className="font-semibold text-amber-600">
                          'Add Word'
                        </span>{" "}
                        to record each completed word
                      </li>
                      <li className="hover:bg-blue-100 p-2 rounded-lg">
                        • Create as many words as possible to earn higher
                        rewards
                      </li>
                      <li className="hover:bg-blue-100 p-2 rounded-lg">
                        • Your words will be automatically submitted when the
                        timer ends - no need of manual submission
                      </li>
                    </ul>
                  </div>
                  <div className="order-1 md:order-2">
                    <img
                      src={game_gif}
                      alt="How to play demonstration"
                      className="rounded-lg w-full shadow-lg transition-transform duration-500 transform hover:scale-105"
                      style={{
                        // aspectRatio: "16/9",
                        imageRendering: "auto",
                      }}
                    />
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-4 p-4 rounded-lg">
                <Timer className="h-6 w-6 text-green-600 mt-1" />
                <div>
                  <p className="font-semibold text-gray-800">Time Limit</p>
                  <p className="text-xl font-bold text-gray-700">
                    {tutorialTime} minute to practice
                  </p>
                  <p className="text-sm text-gray-500 mt-2">
                    Game will automatically submit when time runs out
                  </p>
                </div>
              </div>
            </div>

            {/* Skill Level Slider Section */}
            <div className="mt-24 p-6 bg-red-50 rounded-lg border border-gray-200">
              <h3 className="font-semibold text-gray-800 mb-4">
                How would you rate your skill at word scramble game?
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between text-gray-600 text-sm px-1">
                  <span>Beginner</span>
                  <span>Expert</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={skillLevel}
                  onChange={(e) => setSkillLevel(parseInt(e.target.value))}
                  className="w-full h-2 bg-red-200 rounded-lg appearance-none cursor-pointer accent-red-600"
                />
                <div className="flex justify-between">
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                    <span
                      key={num}
                      className={`h-5 w-5 rounded-full text-xs flex items-center justify-center
                      ${
                        num === skillLevel
                          ? "bg-red-600 text-white"
                          : "text-gray-400"
                      }`}
                    >
                      {num}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <button
              onClick={() => logSkillLevel(skillLevel)}
              disabled={isSubmittingSkill}
              className={`w-full mt-6 py-3 ${
                isSubmittingSkill
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700 cursor-pointer"
              } text-white rounded-lg font-medium transition-colors`}
            >
              {isSubmittingSkill ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                  <span>Submitting...</span>
                </div>
              ) : (
                "Start Practice Round"
              )}
            </button>
          </div>
        </div>
      </Container>
    );
  }

  // Main game view
  return (
    <Container>
      <div className="space-y-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          {notification && (
            <div
              className={`fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50
                ${
                  notification.isError
                    ? "bg-red-100 text-red-700"
                    : "bg-green-100 text-green-700"
                }`}
            >
              {notification.message}
            </div>
          )}

          <GameBoard
            currentWord={gameState.tutorialWord}
            solution={gameState.solution}
            availableLetters={gameState.availableLetters}
            onSolutionChange={(solution, available) =>
              setGameState((prev) => ({
                ...prev,
                solution,
                availableLetters: available,
              }))
            }
            onValidate={handleValidate}
            onSubmit={handleSubmit}
            onRemoveWord={handleRemoveWord}
            wordIndex={0}
            totalWords={1}
            timeLeft={gameState.timeLeft}
            totalTime={gameState.totalTime}
            isTimeUp={gameState.isTimeUp}
            validatedWords={gameState.validatedWords}
            isTutorial={true}
          />

          <EventTrack
            onPageLeave={handlePageLeave}
            onPageReturn={handlePageReturn}
            onInactivityStart={handleInactiveStart}
            onActiveReturn={handleActiveReturn}
            enabled={!showOverview && !isSubmitted.current}
            inactivityTimeout={5000}
          />
        </div>
      </div>
    </Container>
  );
};

export default TutorialGame;
