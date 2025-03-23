import React from "react";
import { CircleAlert } from "lucide-react";

const CoinIcon = ({ className }) => (
  <svg viewBox="0 0 24 24" className={className} fill="currentColor">
    <circle cx="12" cy="12" r="11" fill="currentColor" opacity="0.1" />
    <circle cx="12" cy="12" r="10" fill="currentColor" opacity="0.2" />
    <circle
      cx="12"
      cy="12"
      r="10"
      stroke="currentColor"
      strokeWidth="1.5"
      fill="none"
    />
    <path
      d="M12 2C17.52 2 22 6.48 22 12"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      opacity="0.5"
    />
    <circle
      cx="12"
      cy="12"
      r="7"
      stroke="currentColor"
      strokeWidth="1"
      fill="none"
      opacity="0.3"
    />
    <text
      x="12"
      y="14"
      fontSize="8"
      textAnchor="middle"
      fill="currentColor"
      fontWeight="bold"
    >
      p
    </text>
  </svg>
);

const RewardDisplay = ({ rewards, maxReward }) => {
  const renderCoins = (amount) => {
    const coinElements = [];
    const coinsToShow = Math.min(amount, 15);

    for (let i = 0; i < coinsToShow; i++) {
      coinElements.push(
        <CoinIcon
          key={i}
          className={`h-5 w-5 text-amber-500 transform hover:scale-110 transition-transform duration-200
            ${i > 0 ? "-ml-2" : ""}`}
        />
      );
    }
    return coinElements;
  };

  return (
    <div className="space-y-6">
      <div className="space-y-4 p-4 rounded-lg w-3/5 border border-gray-200 ml-10">
        {Object.entries(rewards)
          .sort(([a], [b]) => Number(b) - Number(a))
          .map(([length, reward]) => (
            <div
              key={length}
              className="flex items-center p-2 bg-white rounded-lg shadow-sm transition-shadow border border-gray-100"
            >
              <span className="text-md font-medium text-gray-800 w-32">
                {length}-letter word
              </span>
              <div className="flex-1 flex items-center gap-2">
                <div className="flex items-center">{renderCoins(reward)}</div>
                <span className="text-amber-600 font-small ml-auto">
                  {reward} pence
                </span>
              </div>
            </div>
          ))}
      </div>

      <div className="bg-yellow-50 p-3 rounded-lg">
        <div className="flex items-center justify-center gap-2 text-yellow-800 text-lg font-medium">
          <CircleAlert className="h-6 w-6" />
          <span>Maximum reward per anagram: {maxReward} pence</span>
        </div>
      </div>
    </div>
  );
};

export default RewardDisplay;
