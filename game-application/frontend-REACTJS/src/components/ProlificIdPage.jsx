import { useState } from "react";
import { Shield } from "lucide-react";
import Container from "./Container";

const ProlificIdPage = ({ onSubmit, initialValue, isInitializing }) => {
  const [id, setId] = useState(initialValue || "");
  const [error, setError] = useState("");

  // // Clear error when ID changes
  // useEffect(() => {
  //   setError("");
  // }, [id]);

  const validateProlificId = (id) => {
    // Basic Prolific ID validation (alphanumeric, correct length)
    const idRegex = /^[0-9a-zA-Z]{24}$/;
    return idRegex.test(id.trim());
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const trimmedId = id.trim();

    if (!trimmedId) {
      setError("Please enter your Prolific ID");
      return;
    }

    if (!validateProlificId(trimmedId)) {
      setError("Please enter a valid 24-character Prolific ID");
      return;
    }

    try {
      await onSubmit(trimmedId);
    } catch (error) {
      setError(
        "You can only participate in this study once. Please contact the researcher if you believe this is a mistake."
      );
    }
  };

  return (
    <Container>
      <div className="max-w-2xl mx-auto space-y-6">
        <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label
                htmlFor="prolificId"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Prolific ID
              </label>
              <input
                id="prolificId"
                type="text"
                value={id}
                onChange={(e) => setId(e.target.value)}
                placeholder="Enter your Prolific ID"
                className={`w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors
                ${error ? "border-red-300 bg-red-50" : "border-gray-300"}`}
                disabled={isInitializing}
                required
              />
              {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
            </div>

            <button
              type="submit"
              disabled={isInitializing || !id.trim()}
              className={`w-full py-3 px-4 rounded-lg font-medium transition-all duration-200 cursor-pointer
              ${
                isInitializing || !id.trim()
                  ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                  : "bg-blue-600 text-white hover:bg-blue-700"
              }`}
            >
              {isInitializing ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                  <span>Initializing...</span>
                </div>
              ) : (
                "Take Me to Practice Round"
              )}
            </button>
          </form>
        </section>
        {/* Privacy Notice */}
        <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 text-sm">
          <div className="flex items-center gap-2 mb-4">
            <Shield className="h-5 w-5 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-800">
              Privacy Notice
            </h3>
          </div>
          <div className="text-gray-600 space-y-2">
            <p>Your Prolific ID will be:</p>
            <ul className="space-y-2">
              <li className="flex items-start">
                <span className="bg-blue-100 rounded-full p-1 mr-2 mt-1">
                  <span className="block h-1.5 w-1.5 bg-blue-600 rounded-full"></span>
                </span>
                Used to track your progress through the study
              </li>
              <li className="flex items-start">
                <span className="bg-blue-100 rounded-full p-1 mr-2 mt-1">
                  <span className="block h-1.5 w-1.5 bg-blue-600 rounded-full"></span>
                </span>
                Stored securely and pseudonymized
              </li>
              <li className="flex items-start">
                <span className="bg-blue-100 rounded-full p-1 mr-2 mt-1">
                  <span className="block h-1.5 w-1.5 bg-blue-600 rounded-full"></span>
                </span>
                Only accessible to the research team
              </li>
            </ul>
          </div>
        </section>
      </div>
    </Container>
  );
};

export default ProlificIdPage;
