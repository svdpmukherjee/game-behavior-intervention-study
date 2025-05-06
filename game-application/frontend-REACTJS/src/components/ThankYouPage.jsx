import { useState } from "react";
import { CheckCircle, ExternalLink, ClipboardCopy } from "lucide-react";
import Container from "./Container";

const ThankYouPage = ({ prolificId, startTime, endTime }) => {
  const [copied, setCopied] = useState(false);

  // Ensure we have valid dates before calculating duration
  const start = startTime ? new Date(startTime) : null;
  const end = endTime ? new Date(endTime) : new Date();
  const duration = start && end ? Math.round((end - start) / 60000) : 0;

  // Get the completion code from environment variables
  const completionCode = import.meta.env.VITE_STUDY_COMPLETION_CODE || "XXXXX";

  // Copy completion code to clipboard
  const copyToClipboard = () => {
    navigator.clipboard.writeText(completionCode).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  // Handle return to Prolific
  const handleReturnToProlific = () => {
    window.location.href = "https://app.prolific.co/submissions/complete";
  };

  return (
    <Container>
      <div className="text-center space-y-6">
        {/* Success Icon */}
        <div className="flex justify-center mb-6">
          <CheckCircle className="h-16 w-16 text-green-500" />
        </div>

        {/* Main Thank You Message */}
        <div>
          <p className="text-lg text-gray-600 mb-6">
            Your responses have been successfully recorded.
          </p>
        </div>

        {/* Study Information */}
        <div className="bg-blue-50 border border-blue-100 rounded-lg p-6 mb-8">
          <h3 className="text-lg font-semibold text-blue-800 mb-3">
            Study Details
          </h3>
          <ul className="text-gray-700 space-y-2">
            <li>
              Your Participant ID:{" "}
              <span className="font-mono bg-blue-100 px-2 py-1 rounded">
                {prolificId}
              </span>
            </li>
            {start && <li>Session started: {start.toLocaleTimeString()}</li>}
            <li>Session ended: {end.toLocaleTimeString()}</li>
            <li>Total duration: {duration} minutes</li>
          </ul>
        </div>

        {/* Study Completion Code Section */}
        <div className="bg-green-50 border border-green-100 rounded-lg p-6 mb-8">
          <h3 className="text-lg font-semibold text-green-800 mb-3">
            Your Study Completion Code
          </h3>
          <div className="flex flex-col items-center gap-3">
            <div className="bg-white px-6 py-3 rounded-lg border border-green-200 font-mono text-lg text-green-700 font-semibold flex items-center gap-3">
              {completionCode}
              <button
                onClick={copyToClipboard}
                className="p-2 bg-green-100 hover:bg-green-200 text-green-700 rounded-lg transition-colors cursor-pointer"
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
              <p className="text-green-600 text-sm">
                Code copied to clipboard!
              </p>
            )}
            <p className="text-gray-700 mt-2">
              Please copy this code and paste it in Prolific to complete the
              study.
            </p>
          </div>
        </div>

        {/* Return to Prolific Button */}
        <div className="mt-8">
          <button
            onClick={handleReturnToProlific}
            className="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-300"
          >
            Return to Prolific and Submit Code
            <ExternalLink className="ml-2 h-5 w-5" />
          </button>
        </div>

        {/* Contact Information */}
        <div className="mt-8 text-sm text-gray-500">
          <p>If you have any questions about this study, please contact:</p>
          <p className="mt-1">
            <a
              href="mailto:suvadeep.mukherjee@uni.lu"
              className="text-blue-600 hover:text-blue-700"
            >
              suvadeep.mukherjee@uni.lu
            </a>
          </p>
        </div>
      </div>
    </Container>
  );
};

export default ThankYouPage;
