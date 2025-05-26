import { useEffect, useRef, useCallback, cloneElement } from "react";

const MouseTracker = ({
  sessionId,
  prolificId,
  currentWord = "",
  currentSolution = [],
  phase = "main_game",
  enabled = true,
  children,
}) => {
  // Simple refs for tracking
  const gameAreaRef = useRef(null);
  const gameAreaBounds = useRef(null);
  const isMouseInGameArea = useRef(false);
  const interactionQueue = useRef([]);
  const flushTimer = useRef(null);
  const sessionCounter = useRef(0);

  // Track hover states
  const activeHovers = useRef(new Map());
  const hoverStartTimes = useRef(new Map());

  // Use refs to track current state for more reliable access
  const currentWordRef = useRef(currentWord);
  const currentSolutionRef = useRef(currentSolution);

  // Update refs when props change
  useEffect(() => {
    currentWordRef.current = currentWord;
    currentSolutionRef.current = currentSolution;
  }, [currentWord, currentSolution]);

  const HOVER_MIN_DURATION = 50;
  const FLUSH_INTERVAL = 2000;

  // Calculate game area bounds
  const calculateGameAreaBounds = useCallback(() => {
    if (!gameAreaRef.current) return null;

    const solutionArea = gameAreaRef.current.querySelector(
      '[data-area="solution-zone"]'
    );
    const availableArea = gameAreaRef.current.querySelector(
      '[data-area="available-zone"]'
    );

    if (!solutionArea || !availableArea) return null;

    const solutionRect = solutionArea.getBoundingClientRect();
    const availableRect = availableArea.getBoundingClientRect();

    const bounds = {
      left: Math.min(solutionRect.left, availableRect.left),
      top: Math.min(solutionRect.top, availableRect.top),
      right: Math.max(solutionRect.right, availableRect.right),
      bottom: Math.max(solutionRect.bottom, availableRect.bottom),
    };

    gameAreaBounds.current = bounds;
    return bounds;
  }, []);

  // Check if point is inside game area
  const isPointInGameArea = useCallback((x, y) => {
    const bounds = gameAreaBounds.current;
    if (!bounds) return false;
    return (
      x >= bounds.left &&
      x <= bounds.right &&
      y >= bounds.top &&
      y <= bounds.bottom
    );
  }, []);

  // Queue interaction
  const queueInteraction = useCallback(
    (type, data) => {
      if (!enabled || !sessionId || !prolificId) return;

      const sessionEventId = ++sessionCounter.current;

      const interaction = {
        sessionId,
        prolificId,
        phase,
        anagramShown: currentWordRef.current,
        interactionType: type,
        timestamp: new Date().toISOString(),
        data: {
          ...data,
          wordInProgress: currentSolutionRef.current.join(""),
          sessionEventId,
        },
      };

      interactionQueue.current.push(interaction);
      // console.log(
      //   `[MouseTracker] Queued ${type} (ID: ${sessionEventId}):`,
      //   data
      // );
    },
    [sessionId, prolificId, phase, enabled]
  );

  // Send queued interactions to backend
  const flushInteractions = useCallback(async () => {
    if (interactionQueue.current.length === 0) return;

    const interactions = [...interactionQueue.current];
    interactionQueue.current = [];

    try {
      await fetch(`${import.meta.env.VITE_API_URL}/api/interactions/batch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId,
          prolificId,
          phase,
          anagramShown: currentWordRef.current,
          interactions,
          batchStartTime:
            interactions[0]?.timestamp || new Date().toISOString(),
          batchEndTime:
            interactions[interactions.length - 1]?.timestamp ||
            new Date().toISOString(),
        }),
      });
    } catch (error) {
      console.error("Failed to send interactions:", error);
      interactionQueue.current = [...interactions, ...interactionQueue.current];
    }
  }, [sessionId, prolificId, phase]);

  // 1. MOUSE MOVEMENT TRACKING - Only track game area entry/exit
  const handleMouseMove = useCallback(
    (e) => {
      if (!enabled) return;

      const wasInside = isMouseInGameArea.current;
      const isInside = isPointInGameArea(e.clientX, e.clientY);
      isMouseInGameArea.current = isInside;

      if (wasInside !== isInside) {
        const bounds = gameAreaBounds.current;
        if (bounds) {
          queueInteraction("mouse_move", {
            x: Math.round(e.clientX - bounds.left),
            y: Math.round(e.clientY - bounds.top),
            isEnteringGameArea: !wasInside && isInside,
            isLeavingGameArea: wasInside && !isInside,
          });
        }
      }
    },
    [enabled, isPointInGameArea, queueInteraction]
  );

  // Create unique element identifier
  const createElementId = useCallback((letter, sourceArea, index) => {
    return `${letter}-${sourceArea}-${index}`;
  }, []);

  // 2. SIMPLIFIED HOVER TRACKING - Independent of drags
  const handleLetterMouseEnter = useCallback(
    (e, letter, sourceArea) => {
      if (!enabled) return;

      const index = e.target.getAttribute("data-index") || "0";
      const elementId = createElementId(letter, sourceArea, index);
      const startTime = Date.now();

      // Store hover start time
      hoverStartTimes.current.set(elementId, startTime);
      activeHovers.current.set(elementId, {
        letter,
        sourceArea,
        index,
        startTime,
      });
    },
    [enabled, createElementId]
  );

  const handleLetterMouseLeave = useCallback(
    (e, letter, sourceArea) => {
      if (!enabled) return;

      const index = e.target.getAttribute("data-index") || "0";
      const elementId = createElementId(letter, sourceArea, index);

      const hoverData = activeHovers.current.get(elementId);
      if (hoverData) {
        const hoverDuration = Date.now() - hoverData.startTime;

        // Record hover if it meets minimum duration
        if (hoverDuration >= HOVER_MIN_DURATION) {
          queueInteraction("letter_hovered", {
            letter: hoverData.letter,
            sourceArea: hoverData.sourceArea,
            hoverDuration,
          });
        }

        // Cleanup
        activeHovers.current.delete(elementId);
        hoverStartTimes.current.delete(elementId);
      }
    },
    [enabled, queueInteraction, createElementId]
  );

  // 3. CLICK-BASED LETTER INTERACTION TRACKING
  // Track user intent to interact with letters via click/mousedown
  const handleLetterClick = useCallback(
    (e, letter, index, sourceArea) => {
      if (!enabled) return;

      // Always record letter interaction when user clicks on it
      // This catches all letter manipulations regardless of drag success/failure
      queueInteraction("letter_dragged", {
        letter,
        sourceArea,
        dragDuration: 0,
      });

      // console.log(
      //   `[MouseTracker] Letter clicked: ${letter} from ${sourceArea}`
      // );
    },
    [enabled, queueInteraction]
  );

  // Setup flush timer
  useEffect(() => {
    if (!enabled) return;

    flushTimer.current = setInterval(() => {
      flushInteractions();
    }, FLUSH_INTERVAL);

    return () => {
      if (flushTimer.current) {
        clearInterval(flushTimer.current);
      }
    };
  }, [enabled, flushInteractions]);

  // Setup mouse move listener and calculate bounds
  useEffect(() => {
    if (!enabled) return;

    const initBounds = () => {
      if (calculateGameAreaBounds()) {
        return true;
      }
      return false;
    };

    if (!initBounds()) {
      const retryInterval = setInterval(() => {
        if (initBounds()) {
          clearInterval(retryInterval);
        }
      }, 100);

      setTimeout(() => clearInterval(retryInterval), 5000);
    }

    document.addEventListener("mousemove", handleMouseMove, { passive: true });

    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
    };
  }, [enabled, calculateGameAreaBounds, handleMouseMove]);

  // Cleanup on unmount or word change
  useEffect(() => {
    return () => {
      flushInteractions();
      activeHovers.current.clear();
      hoverStartTimes.current.clear();

      if (flushTimer.current) {
        clearInterval(flushTimer.current);
      }
    };
  }, [currentWord, flushInteractions]);

  // Reset on word change
  useEffect(() => {
    activeHovers.current.clear();
    hoverStartTimes.current.clear();
  }, [currentWord]);

  if (!children || !enabled) {
    return children || null;
  }

  const Children = cloneElement(children, {
    onLetterMouseEnter: handleLetterMouseEnter,
    onLetterMouseLeave: handleLetterMouseLeave,
    onLetterClick: handleLetterClick,
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
