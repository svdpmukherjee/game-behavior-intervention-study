const Container = ({ children }) => (
  // <div className="min-h-screen bg-gray-100 overflow-x-hidden">
  <div className=" bg-white overflow-x-hidden">
    {/* <div className="py-4 sm:py-6 md:py-8 px-4 sm:px-6 md:px-8 lg:px-10"> */}
    <div>
      <div className="max-w-4xl sm:max-w-5xl md:max-w-6xl lg:max-w-7xl mx-auto w-full">
        <div className="bg-white rounded-lg  p-4 sm:p-6 md:p-8 lg:p-10">
          {children}
        </div>
      </div>
    </div>
  </div>
);

export default Container;
