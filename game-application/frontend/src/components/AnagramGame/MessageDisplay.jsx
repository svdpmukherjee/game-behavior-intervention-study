import { useState, useEffect, useRef } from "react";
import { Info, ArrowRight, AlertTriangle } from "lucide-react";

const MessageDisplay = ({ message, onMessageShown, sessionId, prolificId }) => {
  const [isReady, setIsReady] = useState(false);
  const [hasRead, setHasRead] = useState(false);
  const [studyConfig, setStudyConfig] = useState(null);
  const [error, setError] = useState(null);
  const [visibleSentences, setVisibleSentences] = useState([]);
  const [hasStartedReading, setHasStartedReading] = useState(false);
  const [isAllSentencesVisible, setIsAllSentencesVisible] = useState(false);
  const [showLoader, setShowLoader] = useState(false);
  const [hasReadConfirmed, setHasReadConfirmed] = useState(false);
  const [showGameInfo, setShowGameInfo] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const minReadTime = 10000; // 10 seconds minimum reading time
  const messageStartTime = useRef(null);
  const sentenceDelay = 1000; // 1 second between sentences appearing
  const loaderRemovalDelay = 1000; // 1 second delay before removing loader after last sentence

  // Store sentences from the message
  const sentences = useRef([]);
  const sentenceTimers = useRef([]);

  // Track if message shown event has been logged
  const messageShownLogged = useRef(false);

  // Define the fade-in animation style
  const fadeInStyle = `
    @keyframes slowFadeIn {
      0% { opacity: 0; }
      100% { opacity: 1; }
    }
  `;

  // Log events to the backend
  const logEvent = async (eventType, details = {}) => {
    if (!sessionId || !prolificId || !message?.id) return;

    try {
      const eventBody = {
        sessionId,
        prolificId,
        phase: "main_game",
        eventType,
        details: {
          messageId: message.id,
          messageText: message.text,
          theory: message.theory,
          ...details,
        },
        timestamp: new Date().toISOString(),
      };

      await fetch(`${import.meta.env.VITE_API_URL}/api/game-events`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(eventBody),
      });
    } catch (error) {
      console.error(`Error logging ${eventType}:`, error);
      // Non-blocking error - continue execution even if logging fails
    }
  };

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/study-config`
        );
        if (!response.ok) {
          throw new Error(
            `Failed to fetch study config: ${response.statusText}`
          );
        }
        const data = await response.json();
        setStudyConfig(data);

        // Process sentences after config is loaded
        if (message?.text) {
          sentences.current = message.text
            .split(/(?<=[.!?])\s+|(?<=[.!?])$/)
            .filter((sentence) => sentence.trim().length > 0);
        }
      } catch (error) {
        console.error("Error fetching study config:", error);
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchConfig();
  }, [message?.text]);

  // Prepare the sentences when message changes
  useEffect(() => {
    if (message?.text) {
      // Split text into sentences by periods, question marks, or exclamation marks
      // followed by a space, or at the end of the string
      sentences.current = message.text
        .split(/(?<=[.!?])\s+|(?<=[.!?])$/)
        .filter((sentence) => sentence.trim().length > 0);

      setVisibleSentences([]);
      setIsAllSentencesVisible(false);
      setShowLoader(false);

      // Clear any existing timers
      sentenceTimers.current.forEach((timer) => clearTimeout(timer));
      sentenceTimers.current = [];
    }
  }, [message?.text]);

  // Start revealing sentences when user clicks to see
  useEffect(() => {
    if (hasStartedReading && message?.text) {
      // Show the loader immediately
      setShowLoader(true);

      // Reveal sentences one by one with delay
      sentences.current.forEach((sentence, index) => {
        const timer = setTimeout(() => {
          setVisibleSentences((prev) => [...prev, sentence]);

          // Check if this is the last sentence
          if (index === sentences.current.length - 1) {
            // Keep loader visible for a bit longer after the last sentence
            setTimeout(() => {
              setShowLoader(false);
              setIsAllSentencesVisible(true);
            }, loaderRemovalDelay);
          }
        }, index * sentenceDelay);

        sentenceTimers.current.push(timer);
      });
    }

    return () => {
      // Clear timers on cleanup
      sentenceTimers.current.forEach((timer) => clearTimeout(timer));
    };
  }, [hasStartedReading, message?.text]);

  // Handle minimum reading time
  useEffect(() => {
    if (message?.id && !isReady && hasStartedReading) {
      const timer = setTimeout(() => {
        setIsReady(true);
      }, minReadTime);

      return () => {
        clearTimeout(timer);
      };
    }
  }, [message?.id, hasStartedReading]);

  // Handle completion
  useEffect(() => {
    if (hasRead && message?.id) {
      onMessageShown?.({
        messageId: message.id,
        messageText: message.text,
        theory: message.theory,
      });
    }
  }, [hasRead, message, onMessageShown]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
      </div>
    );
  }

  if (!message?.text) return null;

  if (error) {
    return (
      <div className="text-center p-4 space-y-2">
        <AlertTriangle className="h-6 w-6 text-red-500 mx-auto" />
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!studyConfig) return null;

  const gameTime = studyConfig.timeSettings.game_time / 60;

  // Start revealing sentences and start timer
  const handleStartReading = async () => {
    // Set the start time when user clicks to start reading
    messageStartTime.current = new Date();
    setHasStartedReading(true);

    // Log "motivational_message_shown" event when user clicks to see the message
    if (!messageShownLogged.current) {
      await logEvent("motivational_message_shown");
      messageShownLogged.current = true;
    }
  };

  // Handle checkbox change
  const handleCheckboxChange = () => {
    setHasReadConfirmed(!hasReadConfirmed);
    if (!hasReadConfirmed) {
      setShowGameInfo(true);
    } else {
      setShowGameInfo(false);
    }
  };

  // Handle continue button click
  const handleContinue = async () => {
    // Log "motivational_message_read_complete" event when user finishes reading
    await logEvent("motivational_message_read_complete");

    setHasRead(true);

    // Pass message data to parent component
    onMessageShown?.({
      messageId: message.id,
      messageText: message.text,
      theory: message.theory,
    });
  };

  return (
    <div className="space-y-6">
      <style>{fadeInStyle}</style>

      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 overflow-hidden">
        {/* Message header*/}
        <div className="bg-blue-50 px-6 py-4 rounded-t-lg -mx-6 -mt-6 mb-6 border-b border-blue-100">
          {/* <div className="flex items-center">
            <h3 className="text-xl font-medium text-gray-800">
              A Few Words From The Researcher
            </h3>
          </div> */}
          <div className="flex items-start mt-1">
            <Info className="h-5 w-5 text-blue-600 mr-2 mt-0.5" />
            <h3 className=" text-blue-700">
              Please read this message before proceeding
            </h3>
          </div>
        </div>

        {/* Message content area */}
        <div className="bg-gray-50 p-5 rounded-lg min-h-80">
          {!hasStartedReading ? (
            <div className="flex flex-col items-center justify-center h-full py-10">
              <p className="text-gray-600 text-center mb-12">
                This message contains important information about your word
                creation performance
              </p>
              <button
                onClick={handleStartReading}
                className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors cursor-pointer"
              >
                Curious? See the message now!
              </button>
            </div>
          ) : (
            <div className="space-y-5 min-h-60 p-4">
              <p className="text-gray-500">Hello puzzle-solver!</p>

              {/* Loading indicator for text appearing */}
              <div className="h-2 pl-3">
                {showLoader && (
                  <div className="flex items-center gap-2">
                    <div
                      className="w-1 h-1 bg-blue-500 rounded-full animate-bounce"
                      style={{ animationDelay: "100ms" }}
                    ></div>
                    <div
                      className="w-1 h-1 bg-blue-500 rounded-full animate-bounce"
                      style={{ animationDelay: "300ms" }}
                    ></div>
                    <div
                      className="w-1 h-1 bg-blue-500 rounded-full animate-bounce"
                      style={{ animationDelay: "600ms" }}
                    ></div>
                  </div>
                )}
              </div>

              {/* Sentences that appear one by one */}
              {visibleSentences.map((sentence, index) => (
                <p
                  key={index}
                  className="text-black pl-4 text-lg"
                  style={{
                    animation: "slowFadeIn 2s ease-in-out",
                    opacity: 1,
                  }}
                >
                  {sentence}
                </p>
              ))}
            </div>
          )}
        </div>

        {/* Reading confirmation checkbox - only show after minimum read time */}
        {isAllSentencesVisible && isReady && (
          <div className="mt-4 px-3 py-2 bg-gray-50 rounded-lg">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="readCompletionCheckbox"
                className="h-4 w-4 text-blue-600"
                checked={hasReadConfirmed}
                onChange={handleCheckboxChange}
              />
              <label
                htmlFor="readCompletionCheckbox"
                className="ml-2 text-gray-700 text-sm"
              >
                I have finished reading this message
              </label>
            </div>
          </div>
        )}

        {/* Game info - only show after checkbox is checked */}
        {isReady &&
          isAllSentencesVisible &&
          hasReadConfirmed &&
          showGameInfo && (
            <div className="mt-4 p-3 rounded-lg text-gray-600 text-sm">
              <p>
                You will now solve {studyConfig.game_anagrams} similar word
                creation task for {gameTime} minutes.
              </p>
            </div>
          )}

        {/* Continue button - only show after checkbox is checked */}
        {isReady && isAllSentencesVisible && hasReadConfirmed && (
          <button
            onClick={handleContinue}
            className="w-full mt-5 py-3 rounded-lg font-medium bg-blue-600 hover:bg-blue-700 text-white transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer"
          >
            Continue to next round <ArrowRight className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  );
};

export default MessageDisplay;
