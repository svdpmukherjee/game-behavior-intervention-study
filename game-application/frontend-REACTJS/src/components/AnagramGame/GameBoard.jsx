import React, { useCallback } from "react";
import { Check, X, ArrowDown, ArrowUpCircle } from "lucide-react";
import GameTimer from "./GameTimer";

const GameBoard = ({
  currentWord,
  availableLetters,
  solution,
  onSolutionChange,
  onValidate,
  onSubmit,
  wordIndex,
  totalWords,
  timeLeft,
  totalTime,
  isTimeUp,
  onRemoveWord,
  validatedWords,
  isTutorial = false,
  customSubmitDisabled,
}) => {
  // Handle dragging letters
  const handleDragStart = useCallback((e, letter, index, source) => {
    e.dataTransfer.setData("letter", letter);
    e.dataTransfer.setData("index", index.toString());
    e.dataTransfer.setData("source", source);
  }, []);

  // Handle dropping letters
  const handleDrop = useCallback(
    (e, targetArea, targetIndex) => {
      e.preventDefault();
      const letter = e.dataTransfer.getData("letter");
      const sourceIndex = parseInt(e.dataTransfer.getData("index"));
      const sourceArea = e.dataTransfer.getData("source");

      let newSolution = [...solution];
      let newAvailable = [...availableLetters];

      if (sourceArea === "solution" && targetArea === "solution") {
        // Moving within solution area
        const [removedLetter] = newSolution.splice(sourceIndex, 1);
        newSolution.splice(targetIndex, 0, removedLetter);
      } else if (sourceArea === "available" && targetArea === "solution") {
        // Moving from available to solution
        newAvailable = newAvailable.filter((_, idx) => idx !== sourceIndex);
        newSolution.splice(targetIndex, 0, letter);
      } else if (sourceArea === "solution" && targetArea === "available") {
        // Moving from solution to available
        newSolution = newSolution.filter((_, idx) => idx !== sourceIndex);
        newAvailable.splice(targetIndex, 0, letter);
      }

      onSolutionChange(newSolution, newAvailable);
    },
    [solution, availableLetters, onSolutionChange]
  );

  // Handle clearing the solution
  const handleClearSolution = useCallback(() => {
    if (isTimeUp) return;

    const newAvailable = [...availableLetters, ...solution];
    onSolutionChange([], newAvailable);
  }, [availableLetters, solution, onSolutionChange, isTimeUp]);

  // Handle removing a validated word
  const handleRemoveWord = useCallback(
    (index) => {
      if (typeof onRemoveWord === "function") {
        onRemoveWord(index);
      }
    },
    [onRemoveWord]
  );

  // Calculate maximum solution length (the length of the anagram)
  const maxSolutionLength = currentWord.length;

  // Is validate button disabled
  const isValidateDisabled = solution.length < 5 || (isTimeUp && !isTutorial);

  return (
    <div className="flex flex-col md:flex-row gap-6">
      {/* Main Game Area */}
      <div className="flex-1">
        {/* Game Header */}
        <div className="text-center bg-white rounded-xl mb-16">
          <h2 className="text-xl font-bold text-gray-800">
            Word Creation Challenge {wordIndex + 1} of {totalWords}
          </h2>
          <div className="mt-2 px-4 py-2 bg-blue-50 rounded-lg border border-blue-50 flex items-center justify-center">
            <p className="text-blue-600 text-sm font-medium flex items-center">
              {/* <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 60 30"
                width="60"
                height="30"
                fill="none"
                className="mr-1"
              >
                <path
                  d="M10 15 C20 5, 40 5, 50 15"
                  stroke="#3b82f6"
                  strokeWidth="2"
                  strokeDasharray="4 2"
                />
                <polygon points="46,12 50,15 46,18" fill="#3b82f6" />
              </svg> */}
              Create words with at least 5 letters by drag and drop
            </p>
          </div>
        </div>

        {/* Game Timer */}
        <GameTimer timeLeft={timeLeft} totalTime={totalTime} />

        {/* Solution Area with Numbered Slots */}
        <div className=" px-0 rounded-xl">
          <div className="flex items-center justify-between mb-2 h-8">
            {" "}
            <button
              onClick={handleClearSolution}
              className={`text-red-500 text-sm flex items-center cursor-pointer ml-auto transition-opacity duration-200 ${
                solution.length > 0
                  ? "opacity-100"
                  : "opacity-0 pointer-events-none"
              }`}
              disabled={isTimeUp || solution.length === 0}
            >
              <X className="w-4 h-4 mr-1" /> Clear
            </button>
          </div>

          <div
            className="flex flex-wrap justify-center border-2 border-dashed border-blue-200 rounded-lg bg-blue-50/50 relative w-full min-h-[96px] items-center"
            onDragOver={(e) => e.preventDefault()}
          >
            <div className="absolute -top-3 left-4 bg-white px-3 py-1 text-xs font-semibold text-blue-600 rounded-full border border-blue-200 z-10">
              Drop here
            </div>
            {/* Filled slots */}
            {solution.map((letter, index) => (
              <div
                key={`solution-${index}`}
                draggable={!isTimeUp}
                onDragStart={(e) =>
                  handleDragStart(e, letter, index, "solution")
                }
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => handleDrop(e, "solution", index)}
                className="w-12 h-12  flex flex-col items-center justify-center 
                          font-bold text-xl cursor-move shadow-sm transition-all hover:bg-blue-300 active:scale-95 bg-white border-gray-300 border-1 rounded-sm"
              >
                <span>{letter}</span>
              </div>
            ))}

            {Array.from({ length: maxSolutionLength - solution.length }).map(
              (_, index) => (
                <div
                  key={`empty-${index}`}
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) =>
                    handleDrop(e, "solution", solution.length + index)
                  }
                  className="w-13 h-22 relative"
                >
                  {/* Visual empty slot stays the same size */}
                  <div
                    className="w-12 h-12 border-2 border-dashed border-gray-300 rounded-lg bg-white
                         flex flex-col items-center justify-center text-gray-400 transition-colors hover:bg-gray-50 absolute inset-0 m-auto cursor-move"
                  >
                    {/* <span className="text-gray-300">+</span>
                    <span className="text-xs">
                      {solution.length + index + 1}
                    </span> */}
                  </div>
                </div>
              )
            )}
          </div>
        </div>

        {/* Available Letters Area */}
        <div className="mt-4">
          <div
            className="flex flex-wrap gap-2 justify-center pt-3 border-2 border-green-200 rounded-lg bg-green-50/30 relative w-full min-h-[80px]"
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => handleDrop(e, "available", availableLetters.length)}
          >
            {/* Subtle drag area indicator - left aligned */}
            <span className="absolute -top-3 left-4 bg-white px-3 py-1 text-xs font-semibold text-green-600 rounded-full border border-green-200">
              Drag letters
            </span>
            {availableLetters.map((letter, index) => (
              <div
                key={`available-${index}`}
                draggable={!isTimeUp}
                onDragStart={(e) =>
                  handleDragStart(e, letter, index, "available")
                }
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => handleDrop(e, "available", index)}
                className="w-12 h-12 border-2 border-green-300 bg-gray-700 text-white rounded-lg flex items-center justify-center 
                          font-bold text-xl cursor-move shadow-lg hover:shadow-xl transition-all hover:bg-gray-600 active:scale-95
                          transform hover:-translate-y-1"
                style={{
                  boxShadow: "0 4px 6px rgba(0, 0, 0, 0.3)",
                }}
              >
                {letter}
              </div>
            ))}
          </div>
        </div>

        {/* Action Button */}
        <div className="mt-6">
          <button
            onClick={onValidate}
            disabled={isValidateDisabled}
            className={`
              w-full py-3 rounded-lg font-medium flex items-center justify-center gap-2 transition-all cursor-pointer
              ${
                isValidateDisabled
                  ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                  : "bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white shadow-md hover:shadow-lg"
              }
            `}
          >
            <Check className="w-5 h-5" />
            <span>Add Word</span>
          </button>
        </div>
      </div>

      {/* Right Column - Validated Words */}
      <div className="w-full md:w-64 bg-blue-50 rounded-xl p-4 min-h-[300px]">
        <h3 className="font-semibold text-blue-800 mb-3">
          Your Added Words ({validatedWords.length})
        </h3>
        <div className="flex flex-col gap-2 h-full overflow-y-auto">
          {validatedWords.length > 0 ? (
            validatedWords.map((word, idx) => (
              <div
                key={`validated-${idx}`}
                className="px-3 py-2 bg-white text-blue-700 rounded-lg text-xs font-medium border border-blue-200 shadow-sm flex justify-between items-center"
              >
                <span>{word.word}</span>
                <div className="flex items-center gap-2">
                  <span className="text-blue-500 text-xs">
                    ({word.length} letters)
                  </span>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      handleRemoveWord(idx);
                    }}
                    className="text-red-500 hover:text-red-700 transition-colors cursor-pointer"
                    disabled={isTimeUp}
                  >
                    ×
                  </button>
                </div>
              </div>
            ))
          ) : (
            <p className="text-blue-400 text-sm italic">
              Words you add will appear here
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default React.memo(GameBoard);
