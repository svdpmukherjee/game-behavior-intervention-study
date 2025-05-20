import { useState, useEffect } from "react";
import LandingPage from "./components/LandingPage";
import ProlificIdPage from "./components/ProlificIdPage";
import TutorialGame from "./components/AnagramGame/TutorialGame";
import TestPage from "./components/TestPage";
import SurveyPage from "./components/SurveyPage";
import DebriefPage from "./components/DebriefPage";
import ThankYouPage from "./components/ThankYouPage";
import WordMeaningCheck from "./components/AnagramGame/WordMeaningCheck";
import Container from "./components/Container";
import MessageDisplay from "./components/AnagramGame/MessageDisplay";
import { BadgePoundSterling } from "lucide-react";

const STEPS = {
  LANDING: {
    id: "landing",
    progress: 0,
    title: "Word Puzzles: Test Your Word-Building Skills",
    subtitle: (
      <div className="space-y-2 text-center">
        <p className="text-gray-600 text-md">
          Create valid English words from scrambled letters
        </p>
        <div className="flex flex-col items-center gap-1">
          <p className="text-gray-600 flex items-center gap-1">
            <BadgePoundSterling className="w-5 h-5 text-amber-500" />
            <span className="text-blue-600 font-semibold flex items-center gap-1">
              Longer words{" "}
            </span>{" "}
            earn higher rewards
            <BadgePoundSterling className="w-5 h-5 text-amber-500" />
            <span className="text-blue-600 font-semibold flex items-center gap-1">
              More words{" "}
            </span>{" "}
            earn more rewards
          </p>
        </div>
      </div>
    ),
  },
  PROLIFIC_ID: {
    id: "prolific_id",
    progress: 10,
    step: 1,
    title: "Enter Your Prolific ID to Begin the Study",
  },
  TUTORIAL: {
    id: "tutorial",
    progress: 30,
    step: 2,
    title: "Practice Creating Words",
  },
  MOTIVATIONAL_MESSAGE: {
    id: "motivational_message",
    progress: 45,
    step: 3,
    title: "A Few Words From The Researcher",
  },
  MAIN_GAME: {
    id: "main_game",
    progress: 60,
    step: 4,
    title: "Create Words - Main Round",
  },
  SURVEY: {
    id: "survey",
    progress: 75,
    step: 5,
    title: "Complete a Survey About Your Experience",
  },
  WORD_MEANING: {
    id: "word_meaning",
    progress: 85,
    step: 6,
    title: "Tell Us What Your Created Words Mean to You",
  },
  DEBRIEF: {
    id: "debrief",
    progress: 90,
    step: 7,
    title: "Learn About Your Reward and the Study's Purpose",
  },
  THANK_YOU: {
    id: "thank_you",
    progress: 100,
    title: "Thank You for Participating",
  },
};

function App() {
  const [currentStep, setCurrentStep] = useState(STEPS.LANDING.id);
  const [sessionId, setSessionId] = useState(null);
  const [prolificId, setProlificId] = useState("");
  const [validatedWords, setValidatedWords] = useState([]);
  const [isInitializing, setIsInitializing] = useState(false);
  const [sessionStartTime, setSessionStartTime] = useState(null);
  const [gamePhase, setGamePhase] = useState("loading");
  const [debriefState, setDebriefState] = useState("results");
  const [messageId, setMessageId] = useState(null);
  const [currentMessage, setCurrentMessage] = useState(null);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [currentStep]);

  const handleGamePhaseChange = (phase) => {
    setGamePhase(phase);
  };

  const handleDebriefStateChange = (state) => {
    setDebriefState(state);
  };

  const initializeSession = async (id) => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/initialize-session`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            prolificId: id,
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

      if (!response.ok) throw new Error("Failed to initialize session");
      const data = await response.json();
      return data.sessionId;
    } catch (error) {
      console.error("Session initialization error:", error);
      throw error;
    }
  };

  const handleStartStudy = () => setCurrentStep(STEPS.PROLIFIC_ID.id);

  const handleProlificIdSubmit = async (id) => {
    setIsInitializing(true);
    try {
      setProlificId(id);
      const newSessionId = await initializeSession(id);
      setSessionId(newSessionId);
      setSessionStartTime(new Date());
      setCurrentStep(STEPS.TUTORIAL.id);
    } catch (error) {
      console.error("Error during initialization:", error);
      alert(
        "You can only participate in this study once. Please contact the researcher if you believe this is a mistake."
      );
    } finally {
      setIsInitializing(false);
    }
  };

  const handleTutorialComplete = async () => {
    try {
      // Fetch the motivational message using the game/init endpoint
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/game/init?sessionId=${sessionId}`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch motivational message");
      }

      const data = await response.json();

      // Store the message in state for display
      setCurrentMessage(data.currentMessage);

      // Store the message ID for the survey if it exists
      if (data.currentMessage?.id) {
        setMessageId(data.currentMessage.id);
        console.log("Message ID captured in App:", data.currentMessage.id);
      }

      // Proceed to the motivational message step or main game if no message
      setCurrentStep(
        data.currentMessage ? STEPS.MOTIVATIONAL_MESSAGE.id : STEPS.MAIN_GAME.id
      );
    } catch (error) {
      console.error("Error fetching motivational message:", error);
      // If there's an error, skip to main game
      setCurrentStep(STEPS.MAIN_GAME.id);
    }
  };

  const handleMotivationalMessageComplete = (messageData) => {
    // Store the message ID for the survey if not already stored
    if (messageData.messageId && !messageId) {
      setMessageId(messageData.messageId);
      console.log("Message ID captured in App:", messageData.messageId);
    }

    // Proceed to the main game
    setCurrentStep(STEPS.MAIN_GAME.id);
  };

  const handleMainGameComplete = (words) => {
    setValidatedWords(words);
    setCurrentStep(STEPS.SURVEY.id);
  };

  const handleMessageIdCapture = (id) => {
    if (id) {
      setMessageId(id);
      console.log("Message ID captured in App:", id);
    }
  };

  const handleSurveyComplete = () => {
    setCurrentStep(STEPS.WORD_MEANING.id);
  };

  const handleMeaningCheckComplete = async (meanings) => {
    if (!sessionId || !prolificId) {
      console.error("Missing session ID or Prolific ID");
      alert("Session error. Please try refreshing the page.");
      return;
    }

    if (!meanings || meanings.length === 0) {
      console.log("No word meanings to submit, skipping API call");
      setCurrentStep(STEPS.DEBRIEF.id);
      return;
    }

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/meanings/submit`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sessionId,
            prolificId,
            wordMeanings: meanings || [], // Add fallback
            completedAt: new Date().toISOString(),
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to submit meanings");
      }

      setCurrentStep(STEPS.DEBRIEF.id);
    } catch (error) {
      console.error("Error submitting meanings:", error);
      alert(
        error.message || "Failed to submit word meanings. Please try again."
      );
    }
  };

  const handleDebriefComplete = () => {
    setCurrentStep(STEPS.THANK_YOU.id);
  };

  const getCurrentStep = () => {
    return (
      Object.values(STEPS).find((step) => step.id === currentStep) ||
      STEPS.LANDING
    );
  };

  const renderPage = () => {
    switch (currentStep) {
      case STEPS.LANDING.id:
        return <LandingPage onStartStudy={handleStartStudy} />;

      case STEPS.PROLIFIC_ID.id:
        return (
          <ProlificIdPage
            onSubmit={handleProlificIdSubmit}
            initialValue={prolificId}
            isInitializing={isInitializing}
          />
        );

      case STEPS.TUTORIAL.id:
        return (
          <TutorialGame
            prolificId={prolificId}
            sessionId={sessionId}
            onComplete={handleTutorialComplete}
          />
        );

      case STEPS.MOTIVATIONAL_MESSAGE.id:
        return (
          <MessageDisplay
            message={currentMessage}
            onMessageShown={handleMotivationalMessageComplete}
            sessionId={sessionId}
            prolificId={prolificId}
          />
        );

      case STEPS.MAIN_GAME.id:
        return (
          <TestPage
            prolificId={prolificId}
            sessionId={sessionId}
            onComplete={handleMainGameComplete}
            onPhaseChange={handleGamePhaseChange}
            onMessageIdCapture={handleMessageIdCapture}
          />
        );

      case STEPS.SURVEY.id:
        return (
          <SurveyPage onComplete={handleSurveyComplete} messageId={messageId} />
        );

      case STEPS.WORD_MEANING.id:
        return (
          <WordMeaningCheck
            validatedWords={validatedWords}
            sessionId={sessionId}
            prolificId={prolificId}
            onComplete={handleMeaningCheckComplete}
          />
        );

      case STEPS.DEBRIEF.id:
        return (
          <DebriefPage
            sessionId={sessionId}
            prolificId={prolificId}
            onComplete={handleDebriefComplete}
            onStateChange={handleDebriefStateChange}
          />
        );

      case STEPS.THANK_YOU.id:
        return (
          <ThankYouPage
            prolificId={prolificId}
            startTime={sessionStartTime?.toISOString()}
            endTime={new Date().toISOString()}
          />
        );

      default:
        return <div>Unknown step</div>;
    }
  };

  const currentStepInfo = getCurrentStep();
  const shouldShowTitle = !(
    (currentStep === STEPS.MAIN_GAME.id && gamePhase === "message") ||
    (currentStep === STEPS.DEBRIEF.id && debriefState === "feedback")
  );

  return (
    <div className="min-h-screen bg-white">
      <div className="mx-auto">
        <Container>
          {shouldShowTitle && (
            <div className="text-center mb-8">
              <div className="flex items-center justify-center gap-4 mb-3">
                {currentStepInfo.step && (
                  <span className="inline-flex items-center bg-blue-50 text-blue-600 px-3 py-1 rounded-full text-sm font-medium border border-blue-100">
                    Step {currentStepInfo.step} of{" "}
                    {Object.values(STEPS).length - 2}
                  </span>
                )}
                <h1 className="text-3xl font-bold text-gray-800">
                  {currentStepInfo.title}
                </h1>
              </div>
              <div className="max-w-2xl mx-auto">
                <p className="text-gray-600">{currentStepInfo.subtitle}</p>
              </div>
            </div>
          )}

          {renderPage()}
        </Container>
      </div>
    </div>
  );
}

export default App;
