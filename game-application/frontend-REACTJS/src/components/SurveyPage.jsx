import React, { useState, useEffect } from "react";
import {
  ExternalLink,
  CheckCircle,
  ArrowRight,
  ClipboardCopy,
  AlertTriangle,
} from "lucide-react";
import Container from "./Container";

const SurveyPage = ({ onComplete, messageId = "T1C1" }) => {
  const [surveyCode, setSurveyCode] = useState("");
  const [codeError, setCodeError] = useState(false);
  const [surveyOpened, setSurveyOpened] = useState(false);
  const [copied, setCopied] = useState(false);

  // Copy message ID to clipboard
  const copyToClipboard = () => {
    navigator.clipboard.writeText(messageId).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const handleSurveyCodeSubmit = () => {
    const correctCode = import.meta.env.SURVEY_COMPLETION_CODE || "12345";
    if (surveyCode.trim().toLowerCase() === correctCode.toLowerCase()) {
      setCodeError(false);
      onComplete();
    } else {
      setCodeError(true);
    }
  };

  const handleOpenSurvey = () => {
    window.open("https://ulsurvey.uni.lu/", "_blank");
    setSurveyOpened(true);
  };

  return (
    <Container>
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          {/* Steps Section */}
          <div className="p-5">
            <div className="space-y-8">
              {/* Step 1 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold">
                  1
                </div>
                <div className="flex-1">
                  <p className="font-medium text-gray-800 mb-3">
                    Copy this survey code and{" "}
                    <span className="font-medium">
                      mention it when asked in the survey
                    </span>
                  </p>
                  <div className="flex items-center gap-2 mt-2">
                    <div className="bg-gray-100 px-4 py-2 rounded-lg border border-gray-200 font-mono text-lg text-blue-700 font-semibold">
                      {messageId}
                    </div>
                    <button
                      onClick={copyToClipboard}
                      className="p-2 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-lg transition-colors cursor-pointer"
                      title="Copy to clipboard"
                    >
                      {copied ? (
                        <CheckCircle className="h-5 w-5" />
                      ) : (
                        <ClipboardCopy className="h-5 w-5" />
                      )}
                    </button>
                  </div>
                  {copied && (
                    <p className="text-green-600 text-sm mt-1">
                      Code copied to clipboard!
                    </p>
                  )}
                </div>
              </div>

              {/* Step 2 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold">
                  2
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <p className="font-medium text-gray-800">
                      Go to the survey now
                    </p>
                    <button
                      onClick={handleOpenSurvey}
                      className="inline-flex items-center px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors duration-200 cursor-pointer"
                    >
                      Open <ExternalLink className="ml-1 h-3 w-3" />
                    </button>
                  </div>
                </div>
              </div>

              {/* Step 3 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold">
                  3
                </div>
                <div className="flex-1">
                  <p className="font-medium text-gray-800 mb-2">
                    <span className="font-medium">
                      Enter completion code below once you are finished
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Code Input Section */}
          <div className="p-5 bg-gray-50 border-t border-gray-200">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="text-gray-700 font-medium">
                  Survey Completion Code:
                </label>
                {!surveyOpened && (
                  <div className="text-sm text-amber-600 flex items-center gap-1">
                    <AlertTriangle className="h-4 w-4" />
                    Please complete the survey first
                  </div>
                )}
              </div>

              <div className="relative">
                <input
                  type="text"
                  value={surveyCode}
                  onChange={(e) => {
                    setSurveyCode(e.target.value);
                    setCodeError(false);
                  }}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors
                    ${
                      codeError ? "border-red-300 bg-red-50" : "border-gray-300"
                    }
                    ${surveyOpened ? "bg-white" : "bg-gray-50"}`}
                  placeholder="Enter the completion code from the survey"
                  disabled={!surveyOpened}
                />
                {codeError && (
                  <p className="mt-2 text-sm text-red-600">
                    Invalid code. Please enter the correct code provided in the
                    survey.
                  </p>
                )}
              </div>

              <button
                onClick={handleSurveyCodeSubmit}
                disabled={!surveyOpened || !surveyCode.trim()}
                className={`w-full flex items-center justify-center gap-2 py-3 px-4 rounded-lg font-medium transition-all duration-200  cursor-pointer
                  ${
                    !surveyOpened || !surveyCode.trim()
                      ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                      : "bg-green-600 hover:bg-green-700 text-white"
                  }`}
              >
                Continue <ArrowRight className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </Container>
  );
};

export default SurveyPage;
