import React from "react";
import { AlertTriangle, Monitor, Laptop2 } from "lucide-react";

const DeviceWarning = () => {
  return (
    <div className="space-y-4 mb-6">
      {/* Device Requirements */}
      <div className="bg-red-50 border-l-4 border-red-600 p-5 rounded-lg shadow-sm">
        <div className="flex items-start gap-3">
          <AlertTriangle className="h-6 w-6 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            {/* Title */}
            <h2 className="font-bold text-red-800 flex items-center gap-2">
              Device Requirements
            </h2>
            {/* Final Warning */}
            <p className="mt-4 bg-white text-red-900 px-3 py-2 rounded-lg text-center font-semibold text-sm">
              🚫 Mobile devices & tablets are{" "}
              <span className="underline">not supported</span> and will be
              disqualified
            </p>

            {/* Message */}
            <div className="mt-4 text-red-700 text-sm">
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

      {/* Browser Requirements */}
      <div className="bg-blue-50 border-l-4 border-blue-600 p-5 rounded-lg shadow-sm">
        <div className="flex items-start gap-3">
          <AlertTriangle className="h-6 w-6 text-blue-600 flex-shrink-0 mt-0.5" />
          <div>
            <h2 className="font-bold text-blue-800">Browser Requirements</h2>
            <p className="mt-2 text-blue-700 text-sm">
              For optimal performance, please use one of these browsers:
            </p>
            <div className="mt-3 flex flex-wrap gap-3">
              {/* Chrome Logo */}
              <div className="flex items-center bg-white px-3 py-2 rounded-lg border border-blue-200">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  x="0px"
                  y="0px"
                  width="24"
                  height="24"
                  viewBox="0 0 48 48"
                >
                  <path
                    fill="#4caf50"
                    d="M44,24c0,11.044-8.956,20-20,20S4,35.044,4,24S12.956,4,24,4S44,12.956,44,24z"
                  ></path>
                  <path
                    fill="#ffc107"
                    d="M24,4v20l8,4l-8.843,16c0.317,0,0.526,0,0.843,0c11.053,0,20-8.947,20-20S35.053,4,24,4z"
                  ></path>
                  <path
                    fill="#4caf50"
                    d="M44,24c0,11.044-8.956,20-20,20S4,35.044,4,24S12.956,4,24,4S44,12.956,44,24z"
                  ></path>
                  <path
                    fill="#ffc107"
                    d="M24,4v20l8,4l-8.843,16c0.317,0,0.526,0,0.843,0c11.053,0,20-8.947,20-20S35.053,4,24,4z"
                  ></path>
                  <path
                    fill="#f44336"
                    d="M41.84,15H24v13l-3-1L7.16,13.26H7.14C10.68,7.69,16.91,4,24,4C31.8,4,38.55,8.48,41.84,15z"
                  ></path>
                  <path
                    fill="#dd2c00"
                    d="M7.158,13.264l8.843,14.862L21,27L7.158,13.264z"
                  ></path>
                  <path
                    fill="#558b2f"
                    d="M23.157,44l8.934-16.059L28,25L23.157,44z"
                  ></path>
                  <path
                    fill="#f9a825"
                    d="M41.865,15H24l-1.579,4.58L41.865,15z"
                  ></path>
                  <path
                    fill="#fff"
                    d="M33,24c0,4.969-4.031,9-9,9s-9-4.031-9-9s4.031-9,9-9S33,19.031,33,24z"
                  ></path>
                  <path
                    fill="#2196f3"
                    d="M31,24c0,3.867-3.133,7-7,7s-7-3.133-7-7s3.133-7,7-7S31,20.133,31,24z"
                  ></path>
                </svg>
                <span className="text-sm text-gray-800 px-1">
                  Google Chrome
                </span>
              </div>

              {/* Brave Logo */}
              <div className="flex items-center bg-white px-3 py-2 rounded-lg border border-blue-200">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  x="0px"
                  y="0px"
                  width="24"
                  height="24"
                  viewBox="0 0 48 48"
                >
                  <linearGradient
                    id="yG17B1EwMCiUUe9ON9hI5a_cM42lftaD9Z3_gr1"
                    x1="-329.441"
                    x2="-329.276"
                    y1="-136.877"
                    y2="-136.877"
                    gradientTransform="matrix(217.6 0 0 -255.4727 71694.719 -34944.293)"
                    gradientUnits="userSpaceOnUse"
                  >
                    <stop offset="0" stop-color="#e68e00"></stop>
                    <stop offset=".437" stop-color="#d75500"></stop>
                    <stop offset=".562" stop-color="#cf3600"></stop>
                    <stop offset=".89" stop-color="#d22900"></stop>
                    <stop offset="1" stop-color="#d42400"></stop>
                  </linearGradient>
                  <path
                    fill="url(#yG17B1EwMCiUUe9ON9hI5a_cM42lftaD9Z3_gr1)"
                    fill-rule="evenodd"
                    d="M40.635,13.075l0.984-2.418c0,0-1.252-1.343-2.772-2.865	s-4.74-0.627-4.74-0.627L30.439,3H24h-6.439l-3.667,4.165c0,0-3.22-0.895-4.74,0.627s-2.772,2.865-2.772,2.865l0.984,2.418	l-1.252,3.582c0,0,3.682,13.965,4.114,15.671c0.85,3.358,1.431,4.656,3.846,6.358c2.415,1.701,6.797,4.656,7.512,5.104	C22.301,44.237,23.195,45,24,45c0.805,0,1.699-0.763,2.415-1.21c0.715-0.448,5.098-3.403,7.512-5.104	c2.415-1.701,2.996-3,3.846-6.358c0.431-1.705,4.114-15.671,4.114-15.671L40.635,13.075z"
                    clip-rule="evenodd"
                  ></path>
                  <linearGradient
                    id="yG17B1EwMCiUUe9ON9hI5b_cM42lftaD9Z3_gr2"
                    x1="19.087"
                    x2="31.755"
                    y1="7.685"
                    y2="32.547"
                    gradientUnits="userSpaceOnUse"
                  >
                    <stop offset="0" stop-color="#fff"></stop>
                    <stop offset=".24" stop-color="#f8f8f7"></stop>
                    <stop offset="1" stop-color="#e3e3e1"></stop>
                  </linearGradient>
                  <path
                    fill="url(#yG17B1EwMCiUUe9ON9hI5b_cM42lftaD9Z3_gr2)"
                    fill-rule="evenodd"
                    d="M33.078,9.807c0,0,4.716,5.709,4.716,6.929	s-0.593,1.542-1.19,2.176c-0.597,0.634-3.202,3.404-3.536,3.76c-0.335,0.356-1.031,0.895-0.621,1.866	c0.41,0.971,1.014,2.206,0.342,3.459c-0.672,1.253-1.824,2.089-2.561,1.951c-0.738-0.138-2.471-1.045-3.108-1.459	c-0.637-0.414-2.657-2.082-2.657-2.72c0-0.638,2.088-1.784,2.473-2.044c0.386-0.26,2.145-1.268,2.181-1.663	c0.036-0.396,0.022-0.511-0.497-1.489c-0.519-0.977-1.454-2.281-1.298-3.149c0.156-0.868,1.663-1.319,2.74-1.726	c1.076-0.407,3.148-1.175,3.406-1.295c0.259-0.12,0.192-0.233-0.592-0.308c-0.784-0.074-3.009-0.37-4.012-0.09	c-1.003,0.28-2.717,0.706-2.855,0.932c-0.139,0.226-0.261,0.233-0.119,1.012c0.142,0.779,0.876,4.517,0.948,5.181	c0.071,0.664,0.211,1.103-0.504,1.267c-0.715,0.164-1.919,0.448-2.332,0.448s-1.617-0.284-2.332-0.448	c-0.715-0.164-0.576-0.603-0.504-1.267s0.805-4.402,0.948-5.181c0.142-0.779,0.02-0.787-0.119-1.012	c-0.139-0.226-1.852-0.652-2.855-0.932c-1.003-0.28-3.228,0.016-4.012,0.09c-0.784,0.074-0.851,0.188-0.592,0.308	c0.259,0.119,2.331,0.888,3.406,1.295c1.076,0.407,2.584,0.858,2.74,1.726c0.156,0.868-0.779,2.172-1.298,3.149	c-0.519,0.977-0.533,1.093-0.497,1.489c0.036,0.395,1.795,1.403,2.181,1.663c0.386,0.26,2.473,1.406,2.473,2.044	c0,0.638-2.02,2.306-2.657,2.72c-0.637,0.414-2.37,1.321-3.108,1.459c-0.738,0.138-1.889-0.698-2.561-1.951	c-0.672-1.253-0.068-2.488,0.342-3.459c0.41-0.971-0.287-1.51-0.621-1.866c-0.334-0.356-2.94-3.126-3.536-3.76	c-0.597-0.634-1.19-0.956-1.19-2.176s4.716-6.929,4.716-6.929s3.98,0.761,4.516,0.761c0.537,0,1.699-0.448,2.772-0.806	C23.285,9.404,24,9.401,24,9.401s0.715,0.003,1.789,0.361c1.073,0.358,2.236,0.806,2.772,0.806	C29.098,10.568,33.078,9.807,33.078,9.807z M29.542,31.643c0.292,0.183,0.114,0.528-0.152,0.716	c-0.266,0.188-3.84,2.959-4.187,3.265c-0.347,0.306-0.857,0.812-1.203,0.812c-0.347,0-0.856-0.506-1.203-0.812	c-0.347-0.306-3.921-3.077-4.187-3.265c-0.266-0.188-0.444-0.533-0.152-0.716c0.292-0.183,1.205-0.645,2.466-1.298	c1.26-0.653,2.831-1.208,3.076-1.208c0.245,0,1.816,0.555,3.076,1.208C28.336,30.999,29.25,31.46,29.542,31.643z"
                    clip-rule="evenodd"
                  ></path>
                  <linearGradient
                    id="yG17B1EwMCiUUe9ON9hI5c_cM42lftaD9Z3_gr3"
                    x1="-329.279"
                    x2="-329.074"
                    y1="-140.492"
                    y2="-140.492"
                    gradientTransform="matrix(180.608 0 0 -46.0337 59468.86 -6460.583)"
                    gradientUnits="userSpaceOnUse"
                  >
                    <stop offset="0" stop-color="#e68e00"></stop>
                    <stop offset="1" stop-color="#d42400"></stop>
                  </linearGradient>
                  <path
                    fill="url(#yG17B1EwMCiUUe9ON9hI5c_cM42lftaD9Z3_gr3)"
                    fill-rule="evenodd"
                    d="M34.106,7.165L30.439,3H24h-6.439l-3.667,4.165	c0,0-3.22-0.895-4.74,0.627c0,0,4.293-0.388,5.769,2.015c0,0,3.98,0.761,4.516,0.761c0.537,0,1.699-0.448,2.772-0.806	C23.285,9.404,24,9.401,24,9.401s0.715,0.003,1.789,0.361c1.073,0.358,2.236,0.806,2.772,0.806c0.537,0,4.516-0.761,4.516-0.761	c1.476-2.403,5.769-2.015,5.769-2.015C37.326,6.27,34.106,7.165,34.106,7.165"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                <span className="text-sm text-gray-800 px-1">Brave</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeviceWarning;
