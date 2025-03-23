import { useState, useEffect, useCallback } from "react";
import AnagramGame from "./AnagramGame";
import Container from "./Container";
import { AlertTriangle } from "lucide-react";

const TestPage = ({
  prolificId,
  sessionId: existingSessionId,
  onComplete,
  onPhaseChange,
  onMessageIdCapture,
}) => {
  const [sessionId, setSessionId] = useState(existingSessionId);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  // Initialize session
  const initializeSession = useCallback(async () => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/initialize-session`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            prolificId,
            metadata: {
              browser: navigator.userAgent,
              platform: navigator.platform,
              screenSize: {
                width: window.innerWidth,
                height: window.innerHeight,
              },
            },
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to initialize session");
      }

      const data = await response.json();
      return data.sessionId;
    } catch (error) {
      console.error("Session initialization error:", error);
      throw error;
    }
  }, [prolificId]);

  // Session setup effect
  useEffect(() => {
    let mounted = true;
    const maxRetries = 3;

    const setupSession = async () => {
      if (sessionId) {
        setIsLoading(false);
        return;
      }

      try {
        const newSessionId = await initializeSession();

        if (mounted) {
          setSessionId(newSessionId);
          setIsLoading(false);
          setError(null);
        }
      } catch (err) {
        if (mounted) {
          if (retryCount < maxRetries) {
            console.log(
              `Retrying session initialization (${
                retryCount + 1
              }/${maxRetries})...`
            );
            setRetryCount((prev) => prev + 1);
            // Retry after a short delay
            setTimeout(() => setupSession(), 1000);
          } else {
            setError(
              "Failed to initialize the experiment after multiple attempts. Please refresh and try again."
            );
            setIsLoading(false);
          }
        }
      }
    };

    setupSession();

    return () => {
      mounted = false;
    };
  }, [sessionId, initializeSession, retryCount]);

  // Handle game completion
  const handleGameComplete = useCallback(
    async (validatedWordsList) => {
      if (!sessionId || !prolificId) {
        console.error("Missing session ID or prolific ID");
        return;
      }

      try {
        // Simply call the completion handler with validated words
        onComplete?.(validatedWordsList);
      } catch (err) {
        console.error("Game completion error:", err);
        setError("Failed to complete session. Please try again.");
      }
    },
    [sessionId, prolificId, onComplete]
  );

  const handleGamePhaseChange = (phase) => {
    if (onPhaseChange) {
      onPhaseChange(phase);
    }
  };

  // // Calculate reward based on word length
  // const calculateReward = (length) => {
  //   const rewards = {
  //     5: 2,
  //     6: 5,
  //     7: 10,
  //     8: 15,
  //   };
  //   return rewards[length] || 0;
  // };

  // Render loading state
  if (isLoading) {
    return (
      <Container>
        <div className="flex flex-col items-center justify-center min-h-[200px]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4" />
          <div className="text-gray-600">
            {retryCount > 0
              ? `Retrying initialization... (${retryCount}/3)`
              : "Initializing experiment..."}
          </div>
        </div>
      </Container>
    );
  }

  // Render error state
  if (error) {
    return (
      <Container>
        <div className="flex flex-col items-center justify-center min-h-[200px]">
          <AlertTriangle className="h-12 w-12 text-red-500 mb-4" />
          <div className="text-red-600 mb-4">{error}</div>
          <button
            onClick={() => {
              setRetryCount(0);
              setError(null);
              setIsLoading(true);
            }}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
                     transition-colors duration-200"
          >
            Try Again
          </button>
        </div>
      </Container>
    );
  }

  // Render main game component
  if (!sessionId) {
    return (
      <Container>
        <div className="text-center text-red-600">
          Session initialization failed. Please refresh the page.
        </div>
      </Container>
    );
  }

  return (
    <Container>
      <AnagramGame
        prolificId={prolificId}
        sessionId={sessionId}
        onComplete={handleGameComplete}
        onPhaseChange={handleGamePhaseChange}
        onMessageIdCapture={onMessageIdCapture}
      />
    </Container>
  );
};

export default TestPage;
