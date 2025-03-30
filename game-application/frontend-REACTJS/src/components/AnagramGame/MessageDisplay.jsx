import { useState, useEffect, useRef } from "react";
import { Info, ArrowRight, AlertTriangle } from "lucide-react";

const MessageDisplay = ({ message, onMessageShown }) => {
  const [isReady, setIsReady] = useState(false);
  const [hasRead, setHasRead] = useState(false);
  const [remainingTime, setRemainingTime] = useState(20);
  const [studyConfig, setStudyConfig] = useState(null);
  const [error, setError] = useState(null);
  const [typedSentences, setTypedSentences] = useState([]);
  const [currentSentenceIndex, setCurrentSentenceIndex] = useState(0);
  const [currentSentenceText, setCurrentSentenceText] = useState("");
  const [isTypingComplete, setIsTypingComplete] = useState(false);
  const [hasStartedTyping, setHasStartedTyping] = useState(false);

  const minReadTime = 20000;
  const messageStartTime = useRef(new Date());
  const typingSpeed = 5; // milliseconds per character

  // Refs for typing animation
  const sentences = useRef([]);
  const charIndex = useRef(0);
  const typingTimer = useRef(null);

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

      setTypedSentences([]);
      setCurrentSentenceIndex(0);
      setCurrentSentenceText("");
      charIndex.current = 0;
      setIsTypingComplete(false);

      return () => {
        if (typingTimer.current) {
          clearTimeout(typingTimer.current);
        }
      };
    }
  }, [message?.text]);

  // Start typing animation when user clicks to see
  useEffect(() => {
    if (hasStartedTyping && message?.text) {
      // Start typing the first sentence
      typeSentence(0);

      // Start the message timer when typing begins
      messageStartTime.current = new Date();
    }

    return () => {
      if (typingTimer.current) {
        clearTimeout(typingTimer.current);
      }
    };
  }, [hasStartedTyping]);

  // Function to type a sentence character by character
  const typeSentence = (sentenceIndex) => {
    if (sentenceIndex >= sentences.current.length) {
      setIsTypingComplete(true);
      return;
    }

    const currentSentence = sentences.current[sentenceIndex];
    charIndex.current = 0;

    // Clear the current sentence text
    setCurrentSentenceText("");

    const typeNextChar = () => {
      if (charIndex.current < currentSentence.length) {
        // Update the current text with the entire partial sentence up to this point
        // This ensures the first character is always visible
        setCurrentSentenceText(
          currentSentence.substring(0, charIndex.current + 1)
        );
        charIndex.current++;
        typingTimer.current = setTimeout(typeNextChar, typingSpeed);
      } else {
        // Sentence is complete, add it to the typed sentences and clear current text
        setTypedSentences((prev) => [...prev, currentSentence]);
        setCurrentSentenceText("");

        // Move to the next sentence after a pause
        setTimeout(() => {
          setCurrentSentenceIndex(sentenceIndex + 1);
          typeSentence(sentenceIndex + 1);
        }, 500); // pause between sentences
      }
    };

    typeNextChar();
  };

  useEffect(() => {
    if (message?.id && !isReady && hasStartedTyping) {
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
  }, [message?.id, hasStartedTyping]);

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

  // Start the typing animation
  const handleStartTyping = () => {
    setHasStartedTyping(true);
  };

  // Determine the theory icon
  const getTheoryIcon = () => {
    return <Info className="h-6 w-6 text-blue-500" />;
  };

  // Determine header color based on theory
  const getHeaderColor = () => {
    return "bg-blue-100 text-blue-800";
  };

  // Add blinking cursor effect
  const cursorClass = isTypingComplete
    ? "hidden"
    : "inline-block w-1 h-5 bg-gray-800 ml-1 animate-pulse";

  return (
    <div className="space-y-6">
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

        {/* Message content with typing animation */}
        <div className="bg-gray-50 p-6 rounded-lg min-h-[180px] flex flex-col justify-center">
          {!hasStartedTyping ? (
            <div className="flex flex-col items-center justify-center h-full">
              <button
                onClick={handleStartTyping}
                className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2 shadow-md hover:shadow-lg transform cursor-pointer"
              >
                Curious? See the message now!
              </button>
            </div>
          ) : (
            <div className="space-y-5 min-h-60 shadow-sm p-4">
              <p className="italic text-gray-400"> Hello, curious mind!</p>
              {/* Previously completed sentences */}
              {typedSentences.map((sentence, index) => (
                <p key={index} className="text-lg text-gray-800">
                  {sentence}
                </p>
              ))}

              {/* Currently typing sentence */}
              {currentSentenceText && (
                <p className="text-lg text-gray-800">
                  {currentSentenceText}
                  <span className={cursorClass}></span>
                </p>
              )}
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
          disabled={!isReady || !isTypingComplete || !hasStartedTyping}
          className={`
    w-full mt-6 py-3 rounded-lg font-medium
    transition-all duration-300 flex items-center justify-center gap-2 cursor-pointer
    ${
      isReady && isTypingComplete && hasStartedTyping
        ? "bg-blue-600 hover:bg-blue-700 text-white shadow-md hover:shadow-lg transform hover:-translate-y-1"
        : "bg-gray-100 text-gray-400 cursor-not-allowed"
    }
  `}
        >
          {!hasStartedTyping ? (
            "Please view the message first"
          ) : isReady && isTypingComplete ? (
            <>
              I am ready, Let's continue <ArrowRight className="w-5 h-5" />
            </>
          ) : isTypingComplete ? (
            // `Please wait ${remainingTime} seconds...`
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
              <p>
                You need to wait ({remainingTime} seconds) while the puzzles are
                getting ready.
              </p>
            </div>
            // "Please wait for the message to complete..."
          )}
        </button>
      </div>
    </div>
  );
};

export default MessageDisplay;
