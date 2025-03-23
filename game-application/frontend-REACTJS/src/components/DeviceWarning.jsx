import React from "react";
import { AlertTriangle } from "lucide-react";

const DeviceWarning = () => {
  return (
    <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg mb-6 shadow-md">
      <div className="flex items-start">
        <div className="flex-shrink-0 mt-0.5">
          <AlertTriangle className="h-6 w-6 text-red-500" />
        </div>
        <div className="ml-3">
          <h2 className="text-lg font-bold text-red-800">
            IMPORTANT: Device Requirements
          </h2>
          <div className="mt-2 text-red-700">
            <p className="font-medium">
              This study can ONLY be completed using:
            </p>
            <ul className="list-disc ml-6 mt-2 space-y-1">
              <li>A laptop or desktop computer</li>
              <li>A mouse (required for drag-and-drop interactions)</li>
            </ul>
            <p className="mt-2 font-bold">
              Participants using mobile devices, tablets, or touchpads will be
              disqualified.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeviceWarning;
