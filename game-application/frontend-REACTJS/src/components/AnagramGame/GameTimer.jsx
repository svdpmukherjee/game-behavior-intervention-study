import { Timer } from "lucide-react";

const GameTimer = ({ timeLeft, totalTime }) => {
  const percentage = (timeLeft / totalTime) * 100;
  const isWarning = timeLeft <= 30;

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
  };

  return (
    <div className="w-full max-w-md mx-auto mb-4">
      <div className="flex items-center justify-between mb-1">
        <Timer
          className={`h-5 w-5 ${isWarning ? "text-red-500" : "text-blue-500"}`}
        />
        <span
          className={`font-medium ${
            isWarning ? "text-red-600" : "text-blue-600"
          }`}
        >
          {formatTime(timeLeft)} minutes remaining
        </span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`h-2 rounded-full transition-all duration-1000 ${
            isWarning ? "bg-red-500" : "bg-blue-500"
          }`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default GameTimer;
