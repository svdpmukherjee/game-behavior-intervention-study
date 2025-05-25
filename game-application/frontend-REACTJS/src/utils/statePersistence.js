const STATE_KEY = "gameStudyState";

export const saveAppState = (state) => {
  try {
    const stateToSave = {
      currentStep: state.currentStep,
      sessionId: state.sessionId,
      prolificId: state.prolificId,
      sessionStartTime: state.sessionStartTime,
      messageId: state.messageId,
      validatedWords: state.validatedWords,
      currentMessage: state.currentMessage,
      timestamp: Date.now(),
    };
    localStorage.setItem(STATE_KEY, JSON.stringify(stateToSave));
  } catch (error) {
    console.warn("Failed to save state:", error);
  }
};

export const loadAppState = () => {
  try {
    const saved = localStorage.getItem(STATE_KEY);
    if (!saved) return null;

    const state = JSON.parse(saved);

    // Check if state is not too old (e.g., 24 hours)
    const maxAge = 24 * 60 * 60 * 1000; // 24 hours
    if (Date.now() - state.timestamp > maxAge) {
      clearAppState();
      return null;
    }

    return state;
  } catch (error) {
    console.warn("Failed to load state:", error);
    clearAppState();
    return null;
  }
};

export const clearAppState = () => {
  try {
    localStorage.removeItem(STATE_KEY);
  } catch (error) {
    console.warn("Failed to clear state:", error);
  }
};

export const updateAppState = (updates) => {
  try {
    const current = loadAppState();
    if (current) {
      const updated = { ...current, ...updates, timestamp: Date.now() };
      localStorage.setItem(STATE_KEY, JSON.stringify(updated));
    }
  } catch (error) {
    console.warn("Failed to update state:", error);
  }
};
