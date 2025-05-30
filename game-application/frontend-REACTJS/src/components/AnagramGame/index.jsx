import { useState, useEffect, useCallback, useRef } from "react";
import { memo } from "react";
import GameBoard from "./GameBoard";
import EventTrack from "../shared/EventTrack";
import { AlertTriangle } from "lucide-react";
import MouseTracker from "../shared/MouseTracker";

// Helper function to compare arrays for prop changes
const areArraysEqual = (a, b) => {
  if (a.length !== b.length) return false;
  return a.every((item, index) => item === b[index]);
};

// Memoized GameBoard to prevent unnecessary re-renders
const MemoizedGameBoard = memo(GameBoard, (prevProps, nextProps) => {
  // Compare complex arrays
  const solutionEqual = areArraysEqual(prevProps.solution, nextProps.solution);
  const availableLettersEqual = areArraysEqual(
    prevProps.availableLetters,
    nextProps.availableLetters
  );
  const validatedWordsEqual =
    prevProps.validatedWords.length === nextProps.validatedWords.length &&
    prevProps.validatedWords.every(
      (word, idx) => word.word === nextProps.validatedWords[idx].word
    );

  // Compare primitive props
  const primitivePropsEqual =
    prevProps.currentWord === nextProps.currentWord &&
    prevProps.wordIndex === nextProps.wordIndex &&
    prevProps.totalWords === nextProps.totalWords &&
    prevProps.timeLeft === nextProps.timeLeft &&
    prevProps.totalTime === nextProps.totalTime &&
    prevProps.isTimeUp === nextProps.isTimeUp;

  // Only re-render if something meaningful changed
  return (
    solutionEqual &&
    availableLettersEqual &&
    validatedWordsEqual &&
    primitivePropsEqual
  );
});

const AnagramGame = ({
  prolificId,
  sessionId,
  onComplete,
  onPhaseChange,
  onMessageIdCapture,
}) => {
  // Split large gameState into individual states for better performance
  const [phase, setPhase] = useState("loading");
  const [currentWord, setCurrentWord] = useState("");
  const [solution, setSolution] = useState([]);
  const [availableLetters, setAvailableLetters] = useState([]);
  const [wordIndex, setWordIndex] = useState(0);
  const [totalAnagrams, setTotalAnagrams] = useState(3);
  const [timeLeft, setTimeLeft] = useState(0);
  const [totalTime, setTotalTime] = useState(0);
  const [validatedWords, setValidatedWords] = useState([]);
  const [allValidatedWords, setAllValidatedWords] = useState([]);
  const [isTimeUp, setIsTimeUp] = useState(false);
  const [solutions, setSolutions] = useState({});
  const [notification, setNotification] = useState(null);
  const [isRestoring, setIsRestoring] = useState(false);

  // Additional state
  const [studyConfig, setStudyConfig] = useState(null);
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Mouse movement state
  const [mouseTrackingEnabled, setMouseTrackingEnabled] = useState(true);

  // Refs for tracking
  const startTime = useRef(new Date());
  const gameStartTime = useRef(null);
  const timerRef = useRef(null);
  const isSubmitted = useRef(false);
  const timeUpAlertShown = useRef(false);
  const pendingSubmission = useRef(false);
  const visibilityChangeHandled = useRef(false);
  const saveStateInterval = useRef(null);

  // Notify parent about phase changes
  useEffect(() => {
    if (onPhaseChange) {
      onPhaseChange(phase);
    }
  }, [phase, onPhaseChange]);

  // Fetch study configuration on mount
  useEffect(() => {
    const fetchStudyConfig = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/study-config`
        );
        const config = await response.json();
        setStudyConfig(config);
        setTotalAnagrams(config.game_anagrams);
      } catch (error) {
        console.error("Error fetching study config:", error);
        setError("Failed to load game configuration");
      }
    };
    fetchStudyConfig();
  }, []);

  // Save game state to backend periodically
  const saveGameState = useCallback(async () => {
    if (!sessionId || !prolificId || phase !== "play" || isSubmitted.current) {
      return;
    }

    try {
      const stateToSave = {
        currentWord,
        solution,
        availableLetters,
        validatedWords,
        wordIndex,
        timeLeft,
        totalTime,
        isTimeUp,
        solutions,
        allValidatedWords,
        gameStartTime: gameStartTime.current?.toISOString(),
        isSubmitted: isSubmitted.current,
      };

      await fetch(`${import.meta.env.VITE_API_URL}/api/game-state/save`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId,
          prolificId,
          phase: "main_game",
          gameState: stateToSave,
        }),
      });
    } catch (error) {
      console.error("Failed to save game state:", error);
    }
  }, [
    sessionId,
    prolificId,
    phase,
    currentWord,
    solution,
    availableLetters,
    validatedWords,
    wordIndex,
    timeLeft,
    totalTime,
    isTimeUp,
    solutions,
    allValidatedWords,
  ]);

  // Restore game state from backend
  const restoreGameState = useCallback(async () => {
    if (!sessionId || !prolificId) return false;

    try {
      setIsRestoring(true);
      const response = await fetch(
        `${
          import.meta.env.VITE_API_URL
        }/api/game-state/restore?sessionId=${sessionId}&prolificId=${prolificId}&phase=main_game`
      );

      if (!response.ok) return false;

      const data = await response.json();

      if (data.hasState && data.gameState) {
        const restored = data.gameState;

        // Restore all game state
        setCurrentWord(restored.currentWord || "");
        setSolution(restored.solution || []);
        setAvailableLetters(restored.availableLetters || []);
        setValidatedWords(restored.validatedWords || []);
        setAllValidatedWords(restored.allValidatedWords || []);
        setWordIndex(restored.wordIndex || 0);
        setTimeLeft(restored.timeLeft || 0);
        setTotalTime(restored.totalTime || 0);
        setIsTimeUp(restored.isTimeUp || false);
        setSolutions(restored.solutions || {});

        // Set start time for continued timer
        if (restored.gameStartTime) {
          gameStartTime.current = new Date(restored.gameStartTime);
        }

        // Set phase to play to show the game
        setPhase("play");

        return true;
      }

      return false;
    } catch (error) {
      console.error("Failed to restore game state:", error);
      return false;
    } finally {
      setIsRestoring(false);
    }
  }, [sessionId, prolificId]);

  // Clear saved game state
  const clearGameState = useCallback(async () => {
    if (!sessionId || !prolificId) return;

    try {
      await fetch(
        `${
          import.meta.env.VITE_API_URL
        }/api/game-state/clear?sessionId=${sessionId}&prolificId=${prolificId}&phase=main_game`,
        {
          method: "DELETE",
        }
      );
    } catch (error) {
      console.error("Failed to clear game state:", error);
    }
  }, [sessionId, prolificId]);

  // Show notification with auto-dismiss
  const showNotification = useCallback((message, isError = false) => {
    setNotification({ message, isError });
    setTimeout(() => {
      setNotification(null);
    }, 3000);
  }, []);

  // Calculate reward based on study config - memoized
  const calculateReward = useCallback(
    (wordLength, isValid) => {
      if (!studyConfig?.rewards || !isValid) return 0;
      return studyConfig.rewards[wordLength.toString()] || 0;
    },
    [studyConfig]
  );

  // Log game events - memoized
  const logGameEvent = useCallback(
    async (eventType, details = {}) => {
      try {
        const eventBody = {
          sessionId,
          prolificId,
          phase: "main_game",
          anagramShown: currentWord,
          eventType,
          details: {
            ...details,
            currentWord,
            timeLeft,
            validatedWordsCount: validatedWords.length,
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
    [sessionId, prolificId, currentWord, timeLeft, validatedWords.length]
  );

  // Event tracking callbacks - memoized
  const handleInactiveStart = useCallback(() => {
    console.log("handleInactiveStart called in index.jsx");
    if (!isSubmitted.current && phase === "play") {
      console.log("Logging inactivity event");
      logGameEvent("mouse_inactive_start");
    } else {
      console.log("Inactivity event skipped:", {
        isSubmitted: isSubmitted.current,
        phase,
      });
    }
  }, [logGameEvent, phase]);

  const handleActiveReturn = useCallback(() => {
    if (!isSubmitted.current && phase === "play") {
      logGameEvent("mouse_active");
    }
  }, [logGameEvent, phase]);

  const handlePageLeave = useCallback(
    ({ tabChangeCount, timestamp } = {}) => {
      if (!isSubmitted.current) {
        logGameEvent("page_leave", {
          tabChangeCount,
          timestamp,
          currentWord,
        });
      }
    },
    [logGameEvent, currentWord]
  );

  const handlePageReturn = useCallback(() => {
    if (!isSubmitted.current) {
      logGameEvent("page_return", {
        currentWord,
      });
    }
  }, [logGameEvent, currentWord]);

  // Initialize game - memoized
  const initGame = useCallback(async () => {
    try {
      if (!sessionId) {
        console.error("No session ID provided");
        setError("Session ID is required to initialize game");
        return;
      }

      // Only initialize if we're in loading phase
      if (phase !== "loading") return;

      // First try to restore existing game state
      const restored = await restoreGameState();

      if (restored) {
        // Game state was restored successfully
        return;
      }

      // No existing state, initialize fresh game
      const response = await fetch(
        `${
          import.meta.env.VITE_API_URL
        }/api/game/init?sessionId=${sessionId}&fetch_message=false`
      );
      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.detail || "Failed to initialize game");
      }

      const { word, timeSettings } = responseData;

      // Validate required data
      if (!word || !timeSettings) {
        throw new Error("Invalid game configuration received");
      }

      setPhase("play");
      setCurrentWord(word);
      setSolutions(responseData.solutions);
      setAvailableLetters(word.split(""));
      setTimeLeft(timeSettings.game_time);
      setTotalTime(timeSettings.game_time);
      gameStartTime.current = new Date();

      // Pass message ID to parent component if available
      if (
        responseData.currentMessage?.id &&
        typeof onMessageIdCapture === "function"
      ) {
        onMessageIdCapture(responseData.currentMessage.id);
      }

      await logGameEvent("game_init", {
        currentWord: word,
        timeSettings: timeSettings,
      });
    } catch (error) {
      console.error("Game initialization error:", error);
      setError(error.message || "Failed to initialize game");
      await logGameEvent("game_init_error", {
        error: error.message,
        sessionId,
      });
    }
  }, [sessionId, logGameEvent, phase, onMessageIdCapture, restoreGameState]);

  // Word validation check - memoized
  const isValidWord = useCallback(
    (word) => {
      if (!word || !solutions) return false;
      const wordLength = word.length.toString();
      const solutionsForLength = solutions[wordLength];
      return solutionsForLength?.includes(word.toUpperCase());
    },
    [solutions]
  );

  // Validate a word - memoized with all dependencies
  const handleValidate = useCallback(() => {
    const word = solution.join("");

    if (validatedWords.some((w) => w.word === word)) {
      showNotification("This word has already been recorded", true);
      return;
    }

    const isValid = isValidWord(word);

    // Log the validation attempt
    logGameEvent("word_validation", {
      word,
      wordLength: word.length,
      isValid,
    });

    // Add word to validated list
    setValidatedWords((prev) => [
      ...prev,
      {
        word,
        length: word.length,
        validatedAt: new Date().toISOString(),
        isValid,
      },
    ]);

    // Reset solution and availableLetters
    setSolution([]);
    setAvailableLetters(currentWord.split(""));

    showNotification("Word has been recorded");
  }, [
    solution,
    currentWord,
    validatedWords,
    logGameEvent,
    isValidWord,
    showNotification,
  ]);

  // Remove a word - memoized
  const handleRemoveWord = useCallback(
    async (index) => {
      const removedWord = validatedWords[index];
      if (!removedWord) return;

      await logGameEvent("word_removal", {
        word: removedWord.word,
        wordLength: removedWord.length,
      });

      setValidatedWords((prev) => prev.filter((_, i) => i !== index));
      showNotification(`Removed word: ${removedWord.word}`);
    },
    [validatedWords, logGameEvent, showNotification]
  );

  // Handle solution and available letters change together
  const handleSolutionChange = useCallback((solution, available) => {
    setSolution(solution);
    setAvailableLetters(available);
  }, []);

  // Submit words - memoized
  const handleSubmit = useCallback(async () => {
    if (isSubmitting || (isSubmitted.current && !isTimeUp)) return;

    try {
      setIsSubmitting(true);
      isSubmitted.current = true;

      const currentTimeSpent = Date.now() - startTime.current;

      // Calculate rewards for validated words
      const submittedWords = validatedWords.map((word) => ({
        word: word.word,
        length: word.length,
        reward: calculateReward(word.length, isValidWord(word.word)),
        isValid: isValidWord(word.word),
        validatedAt: word.validatedAt,
        submittedAt: new Date().toISOString(),
      }));

      const totalReward = submittedWords.reduce(
        (sum, w) => sum + (w.reward || 0),
        0
      );

      // Submit words
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/word-submissions`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sessionId,
            prolificId,
            phase: "main_game",
            anagramShown: currentWord,
            submittedWords,
            totalReward,
            timeSpent: currentTimeSpent,
            submittedAt: new Date().toISOString(),
          }),
        }
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to submit words");
      }

      // Update all validated words
      setAllValidatedWords((prev) => [...prev, ...submittedWords]);

      // Log submission
      await logGameEvent("word_submission", {
        wordCount: submittedWords.length,
        words: submittedWords,
        timeSpent: currentTimeSpent,
      });

      // Check if this is the final anagram submission
      if (wordIndex >= totalAnagrams - 1) {
        // Show completion alert before moving to next phase
        alert("You have now completed all puzzles!");

        // Complete the game and clear saved state
        await logGameEvent("game_complete", {
          totalWords: [...allValidatedWords, ...submittedWords].length,
          finalAnagram: currentWord,
        });

        await clearGameState();
        onComplete([...allValidatedWords, ...submittedWords]);
        return;
      }

      // Fetch next anagram
      const nextResponse = await fetch(
        `${
          import.meta.env.VITE_API_URL
        }/api/game/next?sessionId=${sessionId}&currentIndex=${wordIndex}`
      );
      const data = await nextResponse.json();

      if (!nextResponse.ok || !data.word || !data.solutions) {
        throw new Error("Failed to fetch next anagram");
      }

      // Reset game state for next anagram
      setWordIndex((prev) => prev + 1);
      setCurrentWord(data.word);
      setSolutions(data.solutions);
      setSolution([]);
      setAvailableLetters(Array.from(data.word));
      setValidatedWords([]);
      setTimeLeft(totalTime);
      setIsTimeUp(false);

      // Reset alert tracking flags
      timeUpAlertShown.current = false;
      pendingSubmission.current = false;
      visibilityChangeHandled.current = false;
      isSubmitted.current = false;
      startTime.current = new Date();
      gameStartTime.current = new Date();
    } catch (error) {
      console.error("Submission error:", error);
      showNotification("Failed to submit words. Please try again.", true);
      isSubmitted.current = false;
    } finally {
      setIsSubmitting(false);
    }
  }, [
    sessionId,
    prolificId,
    currentWord,
    wordIndex,
    totalAnagrams,
    validatedWords,
    allValidatedWords,
    totalTime,
    isTimeUp,
    isSubmitting,
    calculateReward,
    isValidWord,
    logGameEvent,
    onComplete,
    showNotification,
    clearGameState,
  ]);

  // Handle time up - memoized
  const handleTimeUp = useCallback(() => {
    if (isSubmitting || isSubmitted.current) return;

    try {
      // Show alert only if document is visible
      if (document.visibilityState === "visible") {
        // Set flag before showing alert to prevent double alerts
        timeUpAlertShown.current = true;
        alert("Time's up! All of your added words have been submitted");
        handleSubmit();
      } else {
        // Mark as pending if user is not on the page
        pendingSubmission.current = true;
      }
    } catch (error) {
      console.error("Error in handleTimeUp:", error);
      // Reset flags if submission failed
      timeUpAlertShown.current = false;
      pendingSubmission.current = false;
    }
  }, [handleSubmit, isSubmitting]);

  // Setup periodic state saving
  useEffect(() => {
    if (phase === "play" && !isSubmitted.current) {
      // Save state every 5 seconds during gameplay
      saveStateInterval.current = setInterval(saveGameState, 5000);

      return () => {
        if (saveStateInterval.current) {
          clearInterval(saveStateInterval.current);
        }
      };
    }
  }, [phase, saveGameState]);

  // Also save state whenever game state changes
  useEffect(() => {
    if (phase === "play" && !isSubmitted.current) {
      const timeoutId = setTimeout(saveGameState, 1000); // Debounce saves
      return () => clearTimeout(timeoutId);
    }
  }, [
    phase,
    currentWord,
    solution,
    availableLetters,
    validatedWords,
    wordIndex,
    timeLeft,
    saveGameState,
  ]);

  // Unified visibility change handler
  useEffect(() => {
    function handleVisibilityChange() {
      // Only handle visibility change if:
      // 1. User is coming back to the page (becoming visible)
      // 2. There's a pending submission (timer ran out while they were away)
      // 3. The submission hasn't happened yet
      // 4. Time is up
      if (
        document.visibilityState === "visible" &&
        pendingSubmission.current &&
        !isSubmitted.current &&
        isTimeUp &&
        !timeUpAlertShown.current
      ) {
        // Mark that we've handled this visibility change
        visibilityChangeHandled.current = true;
        pendingSubmission.current = false;

        // Set flag before showing alert to prevent double alerts
        timeUpAlertShown.current = true;

        // Alert with slight delay to ensure DOM is ready
        setTimeout(() => {
          if (!isSubmitted.current) {
            alert("Time's up! All of your added words have been submitted");
            handleSubmit();
          }
        }, 100);
      }
    }

    document.addEventListener("visibilitychange", handleVisibilityChange);
    return () =>
      document.removeEventListener("visibilitychange", handleVisibilityChange);
  }, [isTimeUp, handleSubmit]);

  // Optimized timer effect
  useEffect(() => {
    // Only run the timer when in play phase with time left and not submitted
    if (phase === "play" && timeLeft > 0 && !isSubmitted.current) {
      timerRef.current = setInterval(() => {
        setTimeLeft((prevTime) => {
          // When time is about to run out
          if (prevTime <= 1) {
            clearInterval(timerRef.current);

            // First set time to 0
            setIsTimeUp(true);

            // Then check visibility to determine alert behavior
            const isVisible = document.visibilityState === "visible";

            if (
              isVisible &&
              !timeUpAlertShown.current &&
              !isSubmitted.current
            ) {
              // If visible, handle time up with small delay to allow state updates
              setTimeout(handleTimeUp, 50);
            } else if (!timeUpAlertShown.current) {
              // If not visible, mark as pending for when user returns
              pendingSubmission.current = true;
            }

            return 0;
          }
          return prevTime - 1;
        });
      }, 1000);

      return () => {
        if (timerRef.current) {
          clearInterval(timerRef.current);
          timerRef.current = null;
        }
      };
    }
  }, [phase, timeLeft, handleTimeUp]);

  // Initialize game on mount
  useEffect(() => {
    if (sessionId) {
      initGame();
    }
  }, [sessionId, initGame]);

  // Loading state (including restoration)
  if (isRestoring) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mr-4" />
        <div className="text-gray-600">Restoring your game...</div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="text-center p-6">
        <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <p className="text-red-600 mb-4">{error}</p>
        <button
          onClick={() => {
            setError(null);
            setPhase("loading");
            initGame();
          }}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
                     transition-colors duration-200"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        {notification && (
          <div
            className={`fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
              notification.isError
                ? "bg-red-100 text-red-700"
                : "bg-green-100 text-green-700"
            }`}
          >
            {notification.message}
          </div>
        )}

        {phase === "play" && (
          <MouseTracker
            sessionId={sessionId}
            prolificId={prolificId}
            currentWord={currentWord}
            currentSolution={solution}
            phase="main_game"
            enabled={mouseTrackingEnabled && !isSubmitted.current}
            samplingRate={100}
          >
            <MemoizedGameBoard
              currentWord={currentWord}
              solution={solution}
              availableLetters={availableLetters}
              onSolutionChange={handleSolutionChange}
              onValidate={handleValidate}
              onSubmit={handleSubmit}
              onRemoveWord={handleRemoveWord}
              wordIndex={wordIndex}
              totalWords={totalAnagrams}
              timeLeft={timeLeft}
              totalTime={totalTime}
              isTimeUp={isTimeUp}
              validatedWords={validatedWords}
            />
          </MouseTracker>
        )}

        <EventTrack
          onPageLeave={handlePageLeave}
          onPageReturn={handlePageReturn}
          onInactivityStart={handleInactiveStart}
          onActiveReturn={handleActiveReturn}
          enabled={!isSubmitted.current && phase === "play"}
          inactivityTimeout={5000}
        />
      </div>
    </div>
  );
};

export default AnagramGame;
