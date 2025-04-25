import { useState, useEffect, useRef } from "react";
import { Info, ArrowRight, AlertTriangle } from "lucide-react";

const MessageDisplay = ({ message, onMessageShown }) => {
  const [isReady, setIsReady] = useState(false);
  const [hasRead, setHasRead] = useState(false);
  const [remainingTime, setRemainingTime] = useState(10);
  const [studyConfig, setStudyConfig] = useState(null);
  const [error, setError] = useState(null);
  const [visibleSentences, setVisibleSentences] = useState([]);
  const [hasStartedReading, setHasStartedReading] = useState(false);
  const [isAllSentencesVisible, setIsAllSentencesVisible] = useState(false);
  const [showLoader, setShowLoader] = useState(false);

  const minReadTime = 10000; // 20 seconds minimum reading time
  const messageStartTime = useRef(new Date());
  const sentenceDelay = 1000; // 1 second between sentences appearing
  const loaderRemovalDelay = 1000; // 1 second delay before removing loader after last sentence

  // Store sentences from the message
  const sentences = useRef([]);
  const sentenceTimers = useRef([]);

  // Define the fade-in animation style
  const fadeInStyle = `
    @keyframes slowFadeIn {
      0% { opacity: 0; }
      100% { opacity: 1; }
    }
  `;

  useEffect(() => {
    const fetchConfig = async () => {
      try {
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
      } catch (error) {
        console.error("Error fetching study config:", error);
        setError(error.message);
      }
    };
    fetchConfig();
  }, []);

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
      // Start the message timer when reading begins
      messageStartTime.current = new Date();

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
  }, [hasStartedReading]);

  // Handle minimum reading time
  useEffect(() => {
    if (message?.id && !isReady && hasStartedReading) {
      const timer = setTimeout(() => {
        setIsReady(true);
        setRemainingTime(0);
      }, minReadTime);

      const interval = setInterval(() => {
        setRemainingTime((prev) => Math.max(0, prev - 1));
      }, 1000);

      return () => {
        clearTimeout(timer);
        clearInterval(interval);
      };
    }
  }, [message?.id, hasStartedReading]);

  // Handle completion
  useEffect(() => {
    if (hasRead && message?.id) {
      const timeSpent = Math.round(
        (new Date() - messageStartTime.current) / 1000
      );
      // Ensure we pass the complete message object with all properties
      onMessageShown?.({
        messageId: message.id,
        messageText: message.text,
        timeSpentOnMessage: timeSpent,
        theory: message.theory,
      });
    }
  }, [hasRead, message, onMessageShown]);

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

  // Start revealing sentences
  const handleStartReading = () => {
    setHasStartedReading(true);
  };

  // Determine the theory icon
  const getTheoryIcon = () => {
    return <Info className="h-6 w-6 text-blue-500" />;
  };

  // Determine header color based on theory
  const getHeaderColor = () => {
    return "bg-blue-100 text-blue-800";
  };

  return (
    <div className="space-y-6">
      {/* Add the keyframes style to the component */}
      <style>{fadeInStyle}</style>

      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 overflow-hidden">
        {/* Message header */}
        <div
          className={`${getHeaderColor()} px-6 py-4 rounded-t-lg -mx-6 -mt-6 mb-6 flex items-center`}
        >
          <div className="mr-4">{getTheoryIcon()}</div>
          <div>
            <h3 className="text-xl font-semibold">
              A Few Words From The Researcher Before You Start
            </h3>
          </div>
        </div>

        {/* Message content with sentence-by-sentence reveal */}
        <div className="bg-gray-50 p-6 rounded-lg min-h-[180px] flex flex-col justify-center">
          {!hasStartedReading ? (
            <div className="flex flex-col items-center justify-center h-full">
              <button
                onClick={handleStartReading}
                className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2 shadow-md hover:shadow-lg transform cursor-pointer"
              >
                Curious? See the message now!
              </button>
            </div>
          ) : (
            <div className="space-y-5 min-h-80 shadow-sm p-4">
              <p className="text-gray-400">Hello!</p>

              {/* Fixed position loading indicator right after Hello! */}
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
                  className="text-lg text-gray-800 pl-8"
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

        {/* Next steps section */}
        {isReady && (
          <div className="mt-10 p-4 rounded-lg ">
            <p className="text-gray-600 font-medium">Next Steps:</p>
            <p className="text-gray-400 mt-2">
              You will now solve {studyConfig.game_anagrams} similar word
              puzzles with {gameTime} minutes for each
            </p>
          </div>
        )}

        {/* Continue button */}
        <button
          onClick={() => setHasRead(true)}
          disabled={!isReady || !isAllSentencesVisible || !hasStartedReading}
          className={`
            w-full mt-6 py-3 rounded-lg font-medium
            transition-all duration-300 flex items-center justify-center gap-2 cursor-pointer
            ${
              isReady && isAllSentencesVisible && hasStartedReading
                ? "bg-blue-600 hover:bg-blue-700 text-white shadow-md hover:shadow-lg transform hover:-translate-y-1"
                : "bg-white text-gray-400 cursor-not-allowed"
            }
          `}
        >
          {!hasStartedReading ? (
            ""
          ) : isReady && isAllSentencesVisible ? (
            <>
              I am ready, Let's continue <ArrowRight className="w-5 h-5" />
            </>
          ) : isAllSentencesVisible ? (
            <div className="text-center text-sm italic space-y-2">
              <p className="font-medium text-gray-700">
                Please make sure that you understand the message as it is very
                important for the game.
              </p>
              <p>
                You need to wait ({remainingTime} seconds) while the puzzles are
                getting ready.
              </p>
            </div>
          ) : (
            <div className="text-center text-sm italic space-y-2">
              <p className="font-medium text-gray-700">
                Please make sure that you understand the message as it is very
                important for the game.
              </p>
              <p>Please wait while the message is being revealed...</p>
            </div>
          )}
        </button>
      </div>
    </div>
  );
};

export default MessageDisplay;
