import { CheckCircle, ExternalLink } from "lucide-react";
import Container from "./Container";

const ThankYouPage = ({ prolificId, startTime, endTime }) => {
  // Ensure we have valid dates before calculating duration
  const start = startTime ? new Date(startTime) : null;
  const end = endTime ? new Date(endTime) : new Date();

  const duration = start && end ? Math.round((end - start) / 60000) : 0;

  return (
    <Container>
      <div className="text-center space-y-6">
        {/* Success Icon */}
        <div className="flex justify-center mb-6">
          <CheckCircle className="h-16 w-16 text-green-500" />
        </div>

        {/* Main Thank You Message */}
        <div>
          {/* <h2 className="text-3xl font-bold text-gray-800 mb-4">
            Thank You for Participating!
          </h2> */}
          <p className="text-lg text-gray-600 mb-6">
            Your responses have been successfully recorded.
          </p>
        </div>

        {/* Study Information */}
        <div className="bg-blue-50 border border-blue-100 rounded-lg p-6 mb-8">
          {/* <h3 className="text-lg font-semibold text-blue-800 mb-3">
            Study Details
          </h3> */}
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

        {/* Next Steps */}
        <div className="bg-green-50 border border-green-100 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-green-800 mb-3">
            Next Steps
          </h3>
          <div className="text-gray-700 space-y-2">
            <p>Please return to Prolific and complete the study.</p>
            <p className="text-sm text-gray-500">
              Your earned rewards will be sent out separately.
            </p>
          </div>
        </div>

        {/* Return to Prolific Button */}
        <div className="mt-8">
          <a
            href="https://app.prolific.co"
            rel="noopener noreferrer"
            className="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-300"
          >
            Return to Prolific
            <ExternalLink className="ml-2 h-5 w-5" />
          </a>
        </div>

        {/* Contact Information */}
        <div className="mt-8 text-sm text-gray-500">
          <p>If you have any questions about this study, please contact:</p>
          <p className="mt-1">
            <a
              href="mailto:researcher@uni.lu"
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
