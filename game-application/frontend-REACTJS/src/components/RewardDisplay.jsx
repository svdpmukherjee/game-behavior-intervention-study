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
      <div className="space-y-4 rounded-lg w-4/5 bg-gray-50 border-gray-200 m-auto">
        {Object.entries(rewards)
          .sort(([a], [b]) => Number(b) - Number(a))
          .map(([length, reward]) => (
            <div
              key={length}
              className="flex items-center p-2 bg-white rounded-lg shadow-sm transition-shadow border border-gray-100]"
            >
              <span className="text-md font-medium text-gray-800">
                {length}-letter word
              </span>
              <div className="flex-1 flex items-center gap-2">
                <div className="flex items-center ml-2">
                  {renderCoins(reward)}
                </div>
                <span className="text-amber-600 font-small ml-auto">
                  {reward} pence
                </span>
              </div>
            </div>
          ))}
      </div>

      <div className="p-3 rounded-lg">
        <div className="bg-gradient-to-r text-center rounded-lg p-4">
          <div className="flex items-center justify-center gap-2 text-xl font-semibold text-gray-800">
            <CircleAlert className="h-6 w-6 text-red-600" />
            <span className="text-lg text-gray-700 font-medium">
              Maximum reward is capped per set of scrambled letters:{" "}
              <strong className="text-xl text-red-600">
                {maxReward} pence
              </strong>
            </span>
          </div>
          {/* <div className="mt-4 text-gray-600 text-sm">
            <p>There are 2 sets of scrambled letters</p>
            <p>
              You can earn up to <strong>{maxReward} pence</strong> per set
            </p>
            <p>
              Remember, the reward is capped at 30 pence per set of words you
              create
            </p>
          </div> */}
        </div>
      </div>
    </div>
  );
};

export default RewardDisplay;
