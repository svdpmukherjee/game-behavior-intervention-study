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
  <section className="bg-white p-6 rounded-xl  border-1 border-gray-100">
    <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
      <Target className="h-5 w-5 text-blue-600 mr-2" />
      Your Task
    </h3>
    <div className="p-6 rounded-lg mb-10">
      <ul className="space-y-4 text-md">
        <li className="flex items-start">
          <span className="bg-blue-100 rounded-full p-1 mr-2 mt-0.5">
            <span className="block h-1.5 w-1.5 bg-blue-600 rounded-full"></span>
          </span>
          <span>
            You will be given{" "}
            <span className="font-semibold">{studyConfig.game_anagrams}</span>{" "}
            sets of scrambled letters
          </span>
        </li>
        <li className="flex items-start">
          <span className="bg-blue-100 rounded-full p-1 mr-2 mt-0.5">
            <span className="block h-1.5 w-1.5 bg-blue-600 rounded-full"></span>
          </span>
          <span>
            Use the letters to form valid English words of{" "}
            <span className="font-semibold">
              at least{" "}
              {Math.min(...Object.keys(studyConfig.rewards).map(Number))}{" "}
              letters
            </span>{" "}
            (e.g., 5, 6, 7 or 8-letter words)
          </span>
        </li>
        <li className="flex items-start">
          <span className="bg-blue-100 rounded-full p-1 mr-2 mt-0.5">
            <span className="block h-1.5 w-1.5 bg-blue-600 rounded-full"></span>
          </span>
          <span>
            Try to find{" "}
            <span className="font-semibold">as many words as possible</span>{" "}
            from each set
          </span>
        </li>
        <li className="flex items-start">
          <span className="bg-blue-100 rounded-full p-1 mr-2 mt-0.5">
            <span className="block h-1.5 w-1.5 bg-blue-600 rounded-full"></span>
          </span>
          <span>
            Your words will be{" "}
            <span className="font-semibold">automatically</span> submitted when
            time runs out -{" "}
            <span className="font-semibold">no need submit manually</span>
          </span>
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
    <div className="space-y-8">
      {/* Time Commitment Section */}
      <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
        <div className="flex items-center gap-3 mb-5">
          <Clock className="h-5 w-5 text-green-600" />
          <h4 className="text-xl font-semibold text-gray-800">
            Time Commitment
          </h4>
        </div>
        <div className="space-y-6">
          <ul className="text-sm text-gray-600 space-y-3">
            {[
              {
                label: "Practice round",
                time: studyConfig.timeSettings.tutorial_time / 60,
                words: 1,
                showWords: true,
              },
              {
                label: "Game round",
                time: studyConfig.timeSettings.game_time / 60,
                words: studyConfig.game_anagrams,
                showWords: true,
              },
              {
                label: "Quick survey",
                time: studyConfig.timeSettings.survey_time / 60,
                showWords: false,
              },
            ].map((item, index) => (
              <li key={index} className="flex items-center space-x-3">
                <span className="bg-green-100 rounded-full p-2">
                  <span className="block h-2 w-2 bg-green-600 rounded-full"></span>
                </span>
                <div>
                  <span className="font-semibold">{item.label}</span>{" "}
                  <span className="text-gray-500">
                    {item.showWords
                      ? `(${item.words} word${item.words !== 1 ? "s" : ""}, `
                      : "("}
                    {item.time} minutes)
                  </span>
                </div>
              </li>
            ))}
          </ul>
          <p className="font-medium text-gray-700 mt-4">
            Total time: {Math.ceil(totalTime / 60)} -{" "}
            {Math.ceil(totalTime / 60) + 3} minutes
          </p>
        </div>
      </div>

      {/* Compensation & Rewards Section */}
      <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
        <div className="flex items-center gap-3 mb-5">
          <Banknote className="h-6 w-6 text-amber-600" />
          <h4 className="text-xl font-semibold text-gray-800">
            Compensation & Rewards
          </h4>
        </div>

        {/* Base Compensation */}
        <div className="bg-gradient-to-r from-amber-100 to-yellow-50 border border-amber-300 text-center rounded-lg p-4 shadow-sm">
          <p className="text-lg font-semibold text-amber-800">
            💰 Base Compensation
          </p>
          <p className="text-2xl font-semibold text-gray-900 mt-2">
            {studyConfig.compensation.prolific_rate}
          </p>
        </div>

        {/* Additional Rewards */}
        <div className="mt-6">
          <h5 className="text-sm font-medium text-gray-700 mb-4">
            Additional rewards per{" "}
            <span className="font-semibold">valid word</span> creation:
          </h5>
          <div className="flex justify-center items-center space-y-2 text-sm">
            <RewardDisplay
              rewards={studyConfig.rewards}
              maxReward={studyConfig.compensation.max_reward_per_anagram}
            />
          </div>
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="flex gap-6">
        <button
          onClick={onBack}
          className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 py-3 rounded-lg font-medium transition-all duration-300 flex items-center justify-center gap-2 cursor-pointer"
        >
          <ArrowLeft className="h-5 w-5" />
          Back
        </button>
        <button
          onClick={onNext}
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-all duration-300 flex items-center justify-center gap-2 cursor-pointer"
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
  <div className="space-y-6 text-sm">
    {/* Section: Data Collection and Privacy */}
    <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <div className="flex items-center gap-2 mb-4">
        <Shield className="h-6 w-6 text-blue-600 fill-blue-300" />
        <h3 className="text-xl font-semibold text-gray-800">
          Data Privacy & Consent
        </h3>
      </div>

      <div className="text-gray-700 space-y-4">
        <p>
          We collect the following data to analyze your behavior and
          interactions during the study:
        </p>
        <ul className="list-disc ml-6 space-y-2">
          {[
            "Puzzle-solving patterns and strategies",
            "Response times and game interactions",
            "Survey responses",
            "Basic demographic information",
          ].map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>

        <p>
          Your personal data will be{" "}
          <span className="font-semibold"> anonymized</span> and securely stored
          at the University of Luxembourg.
        </p>
        <p>
          <span className="font-semibold">Only</span> the study researchers will
          have access to your data, and it will be used solely for this research
          project.
        </p>
        <p>Data may be published without identifying you personally.</p>
      </div>
    </section>

    {/* Consent Checkbox & Action Buttons */}
    <div className="bg-gray-50 p-6 rounded-xl border border-gray-200">
      <div className="flex items-center gap-3 mb-6">
        <input
          type="checkbox"
          id="consent"
          checked={isChecked}
          onChange={() => setIsChecked(!isChecked)}
          className="w-5 h-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500 cursor-pointer"
        />
        <label htmlFor="consent" className="text-gray-700">
          I have read the information above and agree to participate in this
          study.
        </label>
      </div>

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
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 cursor-pointer"
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
