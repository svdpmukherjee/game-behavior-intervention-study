import React from "react";
import {
  AlertTriangle,
  Monitor,
  MousePointerClick,
  Laptop2,
} from "lucide-react";

const DeviceWarning = () => {
  return (
    <div className="bg-red-50 border-l-4 border-red-600 p-6 rounded-lg mb-6 shadow-md text-md">
      <div className="flex items-start gap-3">
        {/* Warning Icon */}
        <AlertTriangle className="h-6 w-6 text-red-600 flex-shrink-0" />

        <div>
          {/* Title */}
          <h2 className="font-bold text-red-800 flex items-center gap-2">
            IMPORTANT: Device Requirements
          </h2>
          {/* Final Warning */}
          <p className="mt-4 bg-white text-red-900 px-3 py-2 rounded-lg text-center font-semibold text-sm">
            🚫 Mobile devices & tablets are{" "}
            <span className="underline">not supported</span> and will be
            disqualified
          </p>

          {/* Message */}
          <div className="mt-8 text-red-700 text-sm">
            <p className="">
              To participate in this study, you{" "}
              <span className="font-bold">must</span> use:
            </p>

            <ul className="mt-3 space-y-2">
              <li className="flex items-center gap-2">
                <Laptop2 className="w-5 h-5 text-red-500" />
                <span>
                  A <span className="font-semibold">laptop </span> (with
                  touchpad or a mouse) OR
                </span>
              </li>
              <li className="flex items-center gap-2">
                <Monitor className="w-5 h-5 text-red-500" />
                <span>
                  A <span className="font-semibold">desktop computer</span>{" "}
                  (with a mouse)
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeviceWarning;
