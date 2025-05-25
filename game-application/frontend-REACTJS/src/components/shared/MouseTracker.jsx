import { useEffect, useRef, useCallback, cloneElement } from "react";

const MouseTracker = ({
  sessionId,
  prolificId,
  currentWord = "",
  currentSolution = [],
  phase = "main_game",
  enabled = true,
  minHoverDuration = 100,
  batchInterval = 5000,
  maxBatchSize = 50,
  children,
}) => {
  // Core tracking refs
  const interactionBuffer = useRef([]);
  const hoverStates = useRef(new Map());
  const gameAreaStored = useRef(false);
  const batchTimer = useRef(null);
  const gameAreaRef = useRef(null);
  const isEnabled = useRef(enabled);
  const gameAreaBounds = useRef(null);
  const isMouseInsideGameArea = useRef(false);
  const lastMousePosition = useRef(null);

  // Track enabled state changes
  useEffect(() => {
    isEnabled.current = enabled;
  }, [enabled]);

  // Calculate precise game area bounds
  const calculateGameAreaBounds = useCallback(() => {
    if (!gameAreaRef.current) return null;

    const solutionArea = gameAreaRef.current.querySelector(
      '[data-area="solution-zone"]'
    );
    const availableArea = gameAreaRef.current.querySelector(
      '[data-area="available-zone"]'
    );

    if (!solutionArea || !availableArea) {
      console.warn("Game areas not found for mouse tracking");
      return null;
    }

    const solutionRect = solutionArea.getBoundingClientRect();
    const availableRect = availableArea.getBoundingClientRect();

    const combinedBounds = {
      left: Math.min(solutionRect.left, availableRect.left),
      top: Math.min(solutionRect.top, availableRect.top),
      right: Math.max(solutionRect.right, availableRect.right),
      bottom: Math.max(solutionRect.bottom, availableRect.bottom),
    };

    const bounds = {
      left: combinedBounds.left,
      top: combinedBounds.top,
      width: combinedBounds.right - combinedBounds.left,
      height: combinedBounds.bottom - combinedBounds.top,
    };

    gameAreaBounds.current = bounds;
    return bounds;
  }, []);

  // Store game area bounds in session document
  const storeGameArea = useCallback(async () => {
    if (gameAreaStored.current) return;

    const bounds = calculateGameAreaBounds();
    if (!bounds) return;

    try {
      const gameAreaData = {
        bounds: bounds,
        screenSize: {
          width: window.innerWidth,
          height: window.innerHeight,
        },
        userAgent: navigator.userAgent,
        calculatedAt: new Date().toISOString(),
      };

      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/sessions/${sessionId}/game-area`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(gameAreaData),
        }
      );

      if (response.ok) {
        gameAreaStored.current = true;
        console.log("Game area bounds stored successfully");
      }
    } catch (error) {
      console.error("Failed to store game area bounds:", error);
    }
  }, [sessionId, calculateGameAreaBounds]);

  // Add interaction to buffer
  const bufferInteraction = useCallback(
    (type, data) => {
      if (!isEnabled.current) return;

      const interaction = {
        sessionId,
        prolificId,
        phase,
        anagramShown: currentWord,
        interactionType: type,
        timestamp: new Date().toISOString(), // Changed to ISO string format
        data: {
          ...data,
          wordInProgress: currentSolution.join(""),
        },
      };

      interactionBuffer.current.push(interaction);
      console.log(`Buffered ${type}:`, data);

      if (interactionBuffer.current.length >= maxBatchSize) {
        flushInteractionBuffer();
      }
    },
    [sessionId, prolificId, phase, currentWord, currentSolution, maxBatchSize]
  );

  // Send buffered interactions to backend
  const flushInteractionBuffer = useCallback(async () => {
    if (interactionBuffer.current.length === 0) return;

    const interactionsToSend = [...interactionBuffer.current];
    interactionBuffer.current = [];

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/interactions/batch`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sessionId,
            prolificId,
            phase,
            anagramShown: currentWord,
            interactions: interactionsToSend,
            batchStartTime:
              interactionsToSend[0]?.timestamp || new Date().toISOString(),
            batchEndTime:
              interactionsToSend[interactionsToSend.length - 1]?.timestamp ||
              new Date().toISOString(),
          }),
        }
      );

      if (!response.ok) {
        console.error(
          "Failed to send interaction batch:",
          await response.text()
        );
      } else {
        console.log(
          `Successfully sent ${interactionsToSend.length} interactions`
        );
      }
    } catch (error) {
      console.error("Error sending interaction batch:", error);
    }
  }, [sessionId, prolificId, phase, currentWord]);

  // Get relative position of element within game area
  const getRelativePosition = useCallback((element) => {
    const bounds = gameAreaBounds.current;
    if (!bounds || !element) return { x: 0, y: 0 };

    const rect = element.getBoundingClientRect();
    return {
      x: Math.round(rect.left + rect.width / 2 - bounds.left),
      y: Math.round(rect.top + rect.height / 2 - bounds.top),
    };
  }, []);

  // Normalize area names for consistency
  const normalizeAreaName = useCallback((areaName) => {
    if (!areaName) return "unknown";
    switch (areaName) {
      case "solution-zone":
        return "solution";
      case "available-zone":
        return "available";
      default:
        return areaName;
    }
  }, []);

  // Check if mouse is inside game area
  const isMouseInGameArea = useCallback((x, y) => {
    const bounds = gameAreaBounds.current;
    if (!bounds) return false;

    return (
      x >= bounds.left &&
      x <= bounds.left + bounds.width &&
      y >= bounds.top &&
      y <= bounds.top + bounds.height
    );
  }, []);

  // Mouse movement handler - only tracks when leaving/entering game area
  const handleMouseMove = useCallback(
    (e) => {
      if (!isEnabled.current) return;

      const mouseX = e.clientX;
      const mouseY = e.clientY;
      const wasInside = isMouseInsideGameArea.current;
      const isInside = isMouseInGameArea(mouseX, mouseY);

      // Update tracking state
      isMouseInsideGameArea.current = isInside;

      // Only record when mouse enters or leaves the game area
      if (wasInside !== isInside) {
        const bounds = gameAreaBounds.current;
        if (bounds) {
          bufferInteraction("mouse_move", {
            x: Math.round(mouseX - bounds.left),
            y: Math.round(mouseY - bounds.top),
            pressure: e.pressure || 0,
            isEnteringGameArea: isInside,
            isLeavingGameArea: !isInside,
          });
        }
      }

      lastMousePosition.current = { x: mouseX, y: mouseY };
    },
    [bufferInteraction, isMouseInGameArea]
  );

  // React event handlers for letter interactions
  const handleLetterDragStart = useCallback(
    (e, letter, index, sourceArea) => {
      if (!isEnabled.current) return;

      const target = e.target;
      const startPosition = getRelativePosition(target);

      // Store drag info on the element
      target._dragInfo = {
        letter,
        sourceArea: normalizeAreaName(sourceArea),
        startPosition,
        startTime: Date.now(),
      };

      console.log(
        `🟢 Drag start: ${letter} from ${normalizeAreaName(sourceArea)}`
      );
    },
    [getRelativePosition, normalizeAreaName]
  );

  const handleLetterDragEnd = useCallback(
    (e, letter, index, originalSourceArea) => {
      if (!isEnabled.current) return;

      const target = e.target;
      if (!target._dragInfo) return;

      const dragInfo = target._dragInfo;

      // Method 1: Check the parent container
      let targetArea = null;
      const parentContainer = target.closest("[data-area]");
      if (parentContainer) {
        const areaName = parentContainer.dataset.area;
        if (areaName === "solution-zone") {
          targetArea = "solution";
        } else if (areaName === "available-zone") {
          targetArea = "available";
        } else {
          targetArea = normalizeAreaName(areaName);
        }
      }

      // Method 2: If parent method failed, try finding drop target
      if (!targetArea) {
        const dropTarget = document.elementFromPoint(e.clientX, e.clientY);
        if (dropTarget) {
          const areaElement = dropTarget.closest("[data-area]");
          if (areaElement) {
            const areaName = areaElement.dataset.area;
            if (areaName === "solution-zone") {
              targetArea = "solution";
            } else if (areaName === "available-zone") {
              targetArea = "available";
            } else {
              targetArea = normalizeAreaName(areaName);
            }
          }
        }
      }

      // Method 3: If still no target, check if the element itself moved areas
      if (!targetArea) {
        // Look for the actual letter element in the DOM to see where it ended up
        const gameBoard = document.querySelector('[data-area="game-board"]');
        if (gameBoard) {
          const solutionArea = gameBoard.querySelector(
            '[data-area="solution-zone"]'
          );
          const availableArea = gameBoard.querySelector(
            '[data-area="available-zone"]'
          );

          if (solutionArea && solutionArea.contains(target)) {
            targetArea = "solution";
          } else if (availableArea && availableArea.contains(target)) {
            targetArea = "available";
          }
        }
      }

      const endPosition = getRelativePosition(target);
      const endTime = Date.now();

      console.log(
        `🔵 Drag end: ${letter} from ${dragInfo.sourceArea} to ${
          targetArea || "unknown"
        }`
      );

      // Record the drag event
      bufferInteraction("letter_dragged", {
        letter,
        sourceArea: dragInfo.sourceArea,
        targetArea: targetArea || dragInfo.sourceArea,
        startPosition: dragInfo.startPosition,
        endPosition,
        dragDuration: endTime - dragInfo.startTime,
      });

      // Clean up
      delete target._dragInfo;

      // Immediate flush for important events
      setTimeout(() => flushInteractionBuffer(), 100);
    },
    [
      bufferInteraction,
      getRelativePosition,
      normalizeAreaName,
      flushInteractionBuffer,
    ]
  );

  const handleLetterMouseEnter = useCallback(
    (e, letter, sourceArea) => {
      if (!isEnabled.current) return;

      const letterElement = e.target.closest('[draggable="true"]');
      if (!letterElement) return;

      const normalizedArea = normalizeAreaName(sourceArea);
      const hoverKey = letterElement;

      hoverStates.current.set(hoverKey, {
        letter,
        area: normalizedArea,
        startTime: Date.now(),
      });

      console.log(`🟡 Hover start: ${letter} in ${normalizedArea}`);
    },
    [normalizeAreaName]
  );

  const handleLetterMouseLeave = useCallback(
    (e, letter, sourceArea) => {
      if (!isEnabled.current) return;

      const letterElement = e.target.closest('[draggable="true"]');
      if (!letterElement) return;

      const hoverKey = letterElement;
      const hoverData = hoverStates.current.get(hoverKey);

      if (hoverData) {
        const hoverDuration = Date.now() - hoverData.startTime;

        if (hoverDuration >= minHoverDuration) {
          bufferInteraction("letter_hovered", {
            letter: hoverData.letter,
            sourceArea: hoverData.area,
            hoverDuration,
          });

          console.log(`🟠 Hover end: ${hoverData.letter} (${hoverDuration}ms)`);
        }

        hoverStates.current.delete(hoverKey);
      }
    },
    [bufferInteraction, minHoverDuration]
  );

  // Clean up function
  const cleanup = useCallback(() => {
    // Clear all timers
    if (batchTimer.current) {
      clearInterval(batchTimer.current);
      batchTimer.current = null;
    }

    // Flush remaining interactions
    if (interactionBuffer.current.length > 0) {
      flushInteractionBuffer();
    }

    // Clear hover states
    hoverStates.current.clear();

    console.log("MouseTracker cleaned up");
  }, [flushInteractionBuffer]);

  // Main effect for setting up tracking
  useEffect(() => {
    if (!enabled) return;

    console.log("MouseTracker initializing...");

    // Store game area bounds
    storeGameArea();

    // Calculate initial game area bounds
    setTimeout(() => {
      calculateGameAreaBounds();
    }, 100);

    // Add document-level mouse move listener
    document.addEventListener("mousemove", handleMouseMove, { passive: true });

    // Set up batch timer
    batchTimer.current = setInterval(() => {
      if (interactionBuffer.current.length > 0) {
        flushInteractionBuffer();
      }
    }, batchInterval);

    return () => {
      // Clean up event listeners
      document.removeEventListener("mousemove", handleMouseMove);

      // Clean up timer and flush
      cleanup();
    };
  }, [
    enabled,
    storeGameArea,
    calculateGameAreaBounds,
    handleMouseMove,
    batchInterval,
    flushInteractionBuffer,
    cleanup,
  ]);

  // Reset when word changes
  useEffect(() => {
    if (enabled && interactionBuffer.current.length > 0) {
      flushInteractionBuffer();
    }

    // Clear hover states when word changes
    hoverStates.current.clear();

    // Recalculate game area bounds
    setTimeout(() => {
      calculateGameAreaBounds();
    }, 50);
  }, [currentWord, enabled, flushInteractionBuffer, calculateGameAreaBounds]);

  // Clone children with event handlers
  const Children = cloneElement(children, {
    onLetterDragStart: handleLetterDragStart,
    onLetterDragEnd: handleLetterDragEnd,
    onLetterMouseEnter: handleLetterMouseEnter,
    onLetterMouseLeave: handleLetterMouseLeave,
  });

  return (
    <div
      ref={gameAreaRef}
      data-area="game-board"
      className="w-full h-full relative"
    >
      {Children}
    </div>
  );
};

export default MouseTracker;
