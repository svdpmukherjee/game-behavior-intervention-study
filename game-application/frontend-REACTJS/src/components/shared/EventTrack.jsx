import { useEffect, useRef, useCallback } from "react";

const EventTrack = ({
  onPageLeave,
  onPageReturn,
  onInactivityStart,
  onActiveReturn,
  enabled = true,
  inactivityTimeout = 5000,
}) => {
  const lastActivity = useRef(Date.now());
  const isInactive = useRef(false);
  const pageState = useRef("active");
  const tabChangeCount = useRef(0);
  const lastTabChangeTime = useRef(Date.now());
  const inactivityTimer = useRef(null);
  const lastEventTime = useRef(0);
  const isEnabled = useRef(enabled);
  const isPageHidden = useRef(false); // New ref to track page visibility

  const EVENT_THRESHOLD = 300;
  const TAB_CHANGE_RESET_TIME = 10000;

  const shouldProcessEvent = useCallback(() => {
    const now = Date.now();
    if (now - lastEventTime.current > EVENT_THRESHOLD) {
      lastEventTime.current = now;
      return true;
    }
    return false;
  }, []);

  const clearInactivityTimer = useCallback(() => {
    if (inactivityTimer.current) {
      clearTimeout(inactivityTimer.current);
      inactivityTimer.current = null;
    }
  }, []);

  const checkInactivity = useCallback(() => {
    // Don't check inactivity if page is hidden or inactive
    if (
      !isEnabled.current ||
      isPageHidden.current ||
      pageState.current === "inactive"
    )
      return;

    const now = Date.now();
    const timeSinceLastActivity = now - lastActivity.current;

    if (!isInactive.current && timeSinceLastActivity >= inactivityTimeout) {
      isInactive.current = true;
      onInactivityStart?.();
    }
  }, [inactivityTimeout, onInactivityStart]);

  const resetInactivityTimer = useCallback(() => {
    if (
      !isEnabled.current ||
      isPageHidden.current ||
      pageState.current === "inactive"
    )
      return;

    clearInactivityTimer();

    const now = Date.now();
    lastActivity.current = now;

    if (isInactive.current) {
      isInactive.current = false;
      onActiveReturn?.();
    }

    inactivityTimer.current = setTimeout(checkInactivity, inactivityTimeout);
  }, [
    inactivityTimeout,
    onActiveReturn,
    checkInactivity,
    clearInactivityTimer,
  ]);

  const handleVisibilityChange = useCallback(() => {
    if (!shouldProcessEvent() || !isEnabled.current) return;

    const now = Date.now();
    const hidden = document.hidden;
    isPageHidden.current = hidden; // Update page hidden status

    if (hidden && pageState.current === "active") {
      // Clear inactivity timer when page becomes hidden
      clearInactivityTimer();
      isInactive.current = false; // Reset inactivity state

      tabChangeCount.current++;
      lastTabChangeTime.current = now;
      pageState.current = "inactive";
      onPageLeave?.({
        tabChangeCount: tabChangeCount.current,
        timestamp: now,
      });
    } else if (!hidden && pageState.current === "inactive") {
      pageState.current = "active";
      onPageReturn?.();
      // Reset activity tracking when page becomes visible
      lastActivity.current = now;
      resetInactivityTimer();
    }
  }, [
    onPageLeave,
    onPageReturn,
    resetInactivityTimer,
    shouldProcessEvent,
    clearInactivityTimer,
  ]);

  const handleBlur = useCallback(() => {
    if (!shouldProcessEvent() || !isEnabled.current) return;

    const now = Date.now();
    isPageHidden.current = true; // Set page as hidden
    clearInactivityTimer();
    isInactive.current = false; // Reset inactivity state

    if (pageState.current === "active") {
      pageState.current = "inactive";
      onPageLeave?.({
        tabChangeCount: ++tabChangeCount.current,
        timestamp: now,
      });
    }
  }, [onPageLeave, shouldProcessEvent, clearInactivityTimer]);

  const handleFocus = useCallback(() => {
    if (!shouldProcessEvent() || !isEnabled.current) return;

    isPageHidden.current = false; // Set page as visible

    if (pageState.current === "inactive") {
      pageState.current = "active";
      onPageReturn?.();
      lastActivity.current = Date.now(); // Reset activity timestamp
      resetInactivityTimer();
    }
  }, [onPageReturn, resetInactivityTimer, shouldProcessEvent]);

  const handleActivity = useCallback(
    (e) => {
      if (
        !isEnabled.current ||
        isPageHidden.current ||
        pageState.current === "inactive"
      )
        return;
      resetInactivityTimer();
    },
    [resetInactivityTimer]
  );

  // Track enabled state changes
  useEffect(() => {
    isEnabled.current = enabled;
  }, [enabled]);

  useEffect(() => {
    if (!enabled) return;

    // Set initial page visibility state
    isPageHidden.current = document.hidden;

    // Regular activity checking interval
    const checkInterval = setInterval(() => {
      checkInactivity();
    }, 1000);

    // Document-level event listeners
    document.addEventListener("visibilitychange", handleVisibilityChange);
    window.addEventListener("focus", handleFocus);
    window.addEventListener("blur", handleBlur);

    // Activity tracking events
    const activityEvents = [
      "mousemove",
      "mousedown",
      "keydown",
      "touchstart",
      "scroll",
      "click",
    ];

    activityEvents.forEach((event) => {
      document.addEventListener(event, handleActivity, { passive: true });
    });

    return () => {
      clearInterval(checkInterval);
      clearInactivityTimer();

      document.removeEventListener("visibilitychange", handleVisibilityChange);
      window.removeEventListener("focus", handleFocus);
      window.removeEventListener("blur", handleBlur);

      activityEvents.forEach((event) => {
        document.removeEventListener(event, handleActivity);
      });
    };
  }, [
    enabled,
    handleActivity,
    handleVisibilityChange,
    handleFocus,
    handleBlur,
    checkInactivity,
    clearInactivityTimer,
  ]);

  return null;
};

export default EventTrack;
