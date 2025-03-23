import React, { useCallback } from "react";
import { Check, X } from "lucide-react";
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
        <div className="text-center bg-white rounded-xl mb-4">
          <h2 className="text-xl font-bold text-gray-800">
            Word Challenge {wordIndex + 1} of {totalWords}
          </h2>
          <div className="mt-2 mb-4">
            <p className="text-gray-600">
              Create words with 5+ letters by drag and drop. Added words will be
              submitted when time is up!
            </p>
          </div>
        </div>

        {/* Game Timer */}
        <GameTimer timeLeft={timeLeft} totalTime={totalTime} />

        {/* Solution Area with Numbered Slots */}
        <div className="mt-8 bg-gray-100 pt-3 pl-3 pr-3 rounded-xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-700">Your Word</h3>
            {solution.length > 0 && (
              <button
                onClick={handleClearSolution}
                className="text-red-500 text-sm flex items-center cursor-pointer"
                disabled={isTimeUp}
              >
                <X className="w-4 h-4 mr-1" /> Clear
              </button>
            )}
          </div>

          <div
            className="flex flex-wrap gap-3 justify-center min-h-[80px]"
            onDragOver={(e) => e.preventDefault()}
          >
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
                className="w-12 h-12 bg-blue-600 text-white rounded-lg flex flex-col items-center justify-center 
                          font-bold text-xl cursor-move shadow transition-all hover:bg-blue-700 active:scale-95"
              >
                <span>{letter}</span>
                {/* <span className="text-xs text-blue-50">{index + 1}</span> */}
              </div>
            ))}

            {/* Empty slots */}
            {Array.from({ length: maxSolutionLength - solution.length }).map(
              (_, index) => (
                <div
                  key={`empty-${index}`}
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) =>
                    handleDrop(e, "solution", solution.length + index)
                  }
                  className="w-12 h-12 border-2 border-dashed border-gray-300 rounded-lg 
                         flex flex-col items-center justify-center text-gray-400 transition-colors hover:bg-gray-50"
                >
                  <span className="text-gray-300">+</span>
                  <span className="text-xs">{solution.length + index + 1}</span>
                </div>
              )
            )}
          </div>

          {/* {solution.length > 0 && (
            <div className="text-center mt-4">
              <span className="font-medium text-lg text-blue-600">
                {solution.join("")}
              </span>
            </div>
          )} */}
        </div>

        {/* Available Letters */}
        <div className="mt-8">
          {/* <h3 className="font-semibold text-gray-700 mb-3">
            Available Letters
          </h3> */}
          <div
            className="flex flex-wrap gap-3 justify-center"
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => handleDrop(e, "available", availableLetters.length)}
          >
            {availableLetters.map((letter, index) => (
              <div
                key={`available-${index}`}
                draggable={!isTimeUp}
                onDragStart={(e) =>
                  handleDragStart(e, letter, index, "available")
                }
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => handleDrop(e, "available", index)}
                className="w-12 h-12 bg-gray-700 text-white rounded-lg flex items-center justify-center 
                          font-bold text-xl cursor-move shadow transition-all hover:bg-gray-600 active:scale-95"
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
                  : "bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white shadow hover:shadow-md"
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
