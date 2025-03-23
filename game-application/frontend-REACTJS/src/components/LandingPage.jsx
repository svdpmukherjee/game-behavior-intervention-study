import { useState, useEffect } from "react";
import {
  AlertTriangle,
  Clock,
  Banknote,
  Shield,
  Target,
  ArrowRight,
  ArrowLeft,
} from "lucide-react";
import Container from "./Container";
import CoinIcon from "./CoinIcon";
import RewardDisplay from "./RewardDisplay";
import DeviceWarning from "./DeviceWarning";

const handleExit = () => {
  window.location.href = "https://www.prolific.co";
};

const StudyOverview = ({ onNext, studyConfig }) => (
  <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
    <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
      <Target className="h-5 w-5 text-blue-600 mr-2" />
      Your Task
    </h3>
    <div className=" p-6 rounded-lg mb-10">
      <ul className="space-y-4">
        <li className="flex items-start">
          <span className="bg-blue-100 rounded-full p-1 mr-2 mt-0.5">
            <span className="block h-1.5 w-1.5 bg-blue-600 rounded-full"></span>
          </span>
          <span>
            You will see {studyConfig.game_anagrams} sets of scrambled letters
            and should use them to create valid English words of{" "}
            <span className="font-semibold">
              at least{" "}
              {Math.min(...Object.keys(studyConfig.rewards).map(Number))}{" "}
              letters
            </span>
          </span>
        </li>
        <li className="flex items-start">
          <span className="bg-blue-100 rounded-full p-1 mr-2 mt-0.5">
            <span className="block h-1.5 w-1.5 bg-blue-600 rounded-full"></span>
          </span>
          <span>
            Try to create&nbsp;
            <span className="font-semibold">as many words</span>&nbsp;as you can
            from each set
          </span>
        </li>
        <li className="flex items-start">
          <span className="bg-blue-100 rounded-full p-1 mr-2 mt-0.5">
            <span className="block h-1.5 w-1.5 bg-blue-600 rounded-full"></span>
          </span>
          Your created words will be automatically submitted when the time is up
        </li>
      </ul>
    </div>
    <DeviceWarning />
    <button
      onClick={onNext}
      className="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
    >
      Next
      <ArrowRight className="h-5 w-5" />
    </button>
  </section>
);

const TimeAndCompensation = ({ onNext, onBack, studyConfig }) => {
  if (!studyConfig) return null;

  const totalTime =
    studyConfig.timeSettings.tutorial_time +
    studyConfig.timeSettings.game_time * studyConfig.game_anagrams +
    studyConfig.timeSettings.survey_time;

  return (
    <div className="space-y-6">
      <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div className="flex items-center gap-2 mb-4">
          <Clock className="h-5 w-5 text-green-600" />
          <h4 className="text-lg font-semibold text-gray-800">
            Time Commitment
          </h4>
        </div>
        <div className=" p-4 rounded-lg">
          <ul className="text-md text-gray-600 space-y-3">
            <li className="flex items-center">
              <span className="bg-green-100 rounded-full p-1 mr-2">
                <span className="block h-1.5 w-1.5 bg-green-600 rounded-full"></span>
              </span>
              <div>
                <span className="font-semibold">Practice round</span>{" "}
                <span className="text-gray-500">
                  (1 word, {studyConfig.timeSettings.tutorial_time / 60}{" "}
                  minutes)
                </span>
              </div>
            </li>
            <li className="flex items-center">
              <span className="bg-green-100 rounded-full p-1 mr-2">
                <span className="block h-1.5 w-1.5 bg-green-600 rounded-full"></span>
              </span>
              <div>
                <span className="font-semibold">Game round</span>{" "}
                <span className="text-gray-500">
                  ({studyConfig.game_anagrams} words,{" "}
                  {studyConfig.timeSettings.game_time / 60} minutes each)
                </span>
              </div>
            </li>
            <li className="flex items-center">
              <span className="bg-green-100 rounded-full p-1 mr-2">
                <span className="block h-1.5 w-1.5 bg-green-600 rounded-full"></span>
              </span>
              <div>
                <span className="font-semibold">Quick survey</span>{" "}
                <span className="text-gray-500">
                  ({studyConfig.timeSettings.survey_time / 60} minutes)
                </span>
              </div>
            </li>
          </ul>
          <p className="font-medium text-gray-700 mt-4">
            Total time: ~{Math.ceil(totalTime / 60)} minutes
          </p>
        </div>
      </section>

      <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div className="flex items-center gap-2 mb-4">
          <Banknote className="h-5 w-5 text-amber-600" />
          <h4 className="text-lg font-semibold text-gray-800">Compensation</h4>
        </div>
        <div className="p-4 rounded-lg">
          <p className="font-bold mb-4">
            Base compensation: {studyConfig.compensation.prolific_rate}
          </p>
          <h5 className="font-medium text-gray-700 mb-2">
            Additional rewards per word creation:
          </h5>
          <div className="space-y-2">
            <RewardDisplay
              rewards={studyConfig.rewards}
              maxReward={studyConfig.compensation.max_reward_per_anagram}
            />
          </div>
        </div>
      </section>

      <div className="flex gap-4">
        <button
          onClick={onBack}
          className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
        >
          <ArrowLeft className="h-5 w-5" />
          Back
        </button>
        <button
          onClick={onNext}
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
        >
          Next
          <ArrowRight className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
};

const PrivacyAndConsent = ({
  onBack,
  onStartStudy,
  isChecked,
  setIsChecked,
}) => (
  <div className="space-y-6">
    <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <div className="flex items-center gap-2 mb-4">
        <Shield className="h-6 w-6 text-blue-600 fill-blue-300" />
        <h3 className="text-xl font-semibold text-gray-800">
          Data Collection and Privacy
        </h3>
      </div>

      <div className="space-y-4 text-gray-700">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h4 className="font-medium mb-2">We collect:</h4>
          <ul className="space-y-2 ml-4">
            {[
              "Anagrams you solve and the patterns in solving them",
              "Response times and word creation strategies",
              "Game interactions",
              "Survey responses",
              "Basic demographic information",
            ].map((item, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="bg-blue-100 rounded-full p-1 mt-1">
                  <span className="block h-1.5 w-1.5 bg-blue-600 rounded-full"></span>
                </span>
                {item}
              </li>
            ))}
          </ul>
        </div>

        <div className="space-y-3">
          <p className="flex items-start gap-2">
            <Shield className="h-5 w-5 text-blue-600 flex-shrink-0 " />
            Your personal data will be strictly pseudonymized and securely
            stored at the University of Luxembourg.
          </p>
          <p className="flex items-start gap-2">
            <Shield className="h-5 w-5 text-blue-600 flex-shrink-0 " />
            Only the researchers working on this study will have access to these
            data.
          </p>
          <p className="flex items-start gap-2">
            <Shield className="h-5 w-5 text-blue-600 flex-shrink-0 " />
            The data collected during the study will only be used for the
            research project.
          </p>
          <p className="flex items-start gap-2">
            <Shield className="h-5 w-5 text-blue-600 flex-shrink-0 " />
            The data will be used for publications without personally
            identifying you.
          </p>
        </div>
      </div>
    </section>

    <div className="bg-gray-50 p-6 rounded-xl border border-gray-200">
      <div className="flex items-center gap-3 mb-6">
        <input
          type="checkbox"
          id="consent"
          checked={isChecked}
          onChange={() => setIsChecked(!isChecked)}
          className="w-5 h-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
        />
        <label htmlFor="consent" className="text-gray-700">
          I have read the above information and agree to participate in this
          study
        </label>
      </div>

      {/* Buttons for Back and Start Study */}
      <div className="flex gap-4 mb-4">
        <button
          onClick={onBack}
          className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
        >
          <ArrowLeft className="h-5 w-5" />
          Back
        </button>
        <button
          onClick={onStartStudy}
          disabled={!isChecked}
          className={`
        flex-1 py-3 rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer
        ${
          isChecked
            ? "bg-blue-600 hover:bg-blue-700 text-white"
            : "bg-gray-200 text-gray-500 cursor-not-allowed"
        }
      `}
        >
          Start Study
          <ArrowRight className="h-5 w-5" />
        </button>
      </div>

      <button
        onClick={() => {
          if (window.confirm("Are you sure you want to exit?")) {
            handleExit();
          }
        }}
        className="w-full mt-4 px-8 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium cursor-pointer"
      >
        I do not want to participate
      </button>
    </div>
  </div>
);

const LandingPage = ({ onStartStudy }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [studyConfig, setStudyConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isChecked, setIsChecked] = useState(false);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [currentPage]);

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
      } finally {
        setLoading(false);
      }
    };
    fetchConfig();
  }, []);

  if (loading) {
    return (
      <Container>
        <div className="flex flex-col items-center justify-center min-h-[200px]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4" />
          <div className="text-gray-600">Loading study information...</div>
        </div>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <div className="text-center space-y-4">
          <AlertTriangle className="h-12 w-12 text-red-500 mx-auto" />
          <h2 className="text-xl font-semibold text-red-600">
            Failed to Load Study
          </h2>
          <p className="text-gray-600">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
          >
            Try Again
          </button>
        </div>
      </Container>
    );
  }

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 1:
        return (
          <StudyOverview
            studyConfig={studyConfig}
            onNext={() => setCurrentPage(2)}
          />
        );
      case 2:
        return (
          <TimeAndCompensation
            studyConfig={studyConfig}
            onNext={() => setCurrentPage(3)}
            onBack={() => setCurrentPage(1)}
          />
        );
      case 3:
        return (
          <PrivacyAndConsent
            onBack={() => setCurrentPage(2)}
            onStartStudy={onStartStudy}
            isChecked={isChecked}
            setIsChecked={setIsChecked}
          />
        );
    }
  };

  return (
    <Container>
      <div className="max-w-4xl mx-auto space-y-6 mb-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-xl font-bold text-gray-800">
            {currentPage === 1 && "Study Details"}
            {currentPage === 2 && "Study Details"}
            {currentPage === 3 && "Study Details"}
          </h1>
        </div>

        {renderCurrentPage()}
      </div>
    </Container>
  );
};

export default LandingPage;
