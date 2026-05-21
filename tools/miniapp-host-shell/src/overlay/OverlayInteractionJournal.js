/**
 * OverlayInteractionJournal — DEP-OVR-005
 * Structured JSON event emitter for AI host awareness.
 * Emits on state transitions ONLY — per-frame emission is explicitly forbidden (AC-25E).
 * Events delivered to backend via batch submission or WebSocket channel.
 */

export class OverlayInteractionJournal {
  constructor({ sessionId, onEmit }) {
    this._sessionId = sessionId;
    this._onEmit = onEmit || (() => {});
    this._events = [];
    this._batchQueue = [];
    this._batchInterval = null;
    this._batchIntervalMs = 5000;
  }

  emit({ eventType, roundIndex = null, fromState = null, toState = null, overlayElements = {}, captureState = {} }) {
    const event = {
      event_type: eventType,
      session_id: this._sessionId,
      timestamp_ms: Date.now(),
      round_index: roundIndex,
      from_state: fromState,
      to_state: toState,
      overlay_elements: overlayElements,
      capture_state: captureState,
      receipt_id: null,
    };

    this._events.push(event);
    this._batchQueue.push(event);
    this._onEmit(event);
  }

  startBatchSubmission(submitFn) {
    this._batchInterval = setInterval(() => {
      if (this._batchQueue.length > 0) {
        const batch = [...this._batchQueue];
        this._batchQueue = [];
        submitFn(batch);
      }
    }, this._batchIntervalMs);
  }

  stopBatchSubmission() {
    if (this._batchInterval) {
      clearInterval(this._batchInterval);
      this._batchInterval = null;
    }
  }

  flush(submitFn) {
    if (this._batchQueue.length > 0) {
      const batch = [...this._batchQueue];
      this._batchQueue = [];
      submitFn(batch);
    }
  }

  getEvents() {
    return [...this._events];
  }

  getEventCount() {
    return this._events.length;
  }

  persistToLocalStorage() {
    try {
      const key = `overlay_journal_${this._sessionId}`;
      localStorage.setItem(key, JSON.stringify(this._events));
    } catch {
      // Storage quota exceeded — silently degrade
    }
  }

  restoreFromLocalStorage() {
    try {
      const key = `overlay_journal_${this._sessionId}`;
      const data = localStorage.getItem(key);
      if (data) {
        const parsed = JSON.parse(data);
        this._events = parsed;
        return parsed;
      }
    } catch {
      // Parse failure — start fresh
    }
    return [];
  }

  destroy() {
    this.stopBatchSubmission();
    this._events = [];
    this._batchQueue = [];
  }
}
