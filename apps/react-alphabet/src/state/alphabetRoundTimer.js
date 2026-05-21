export function startRoundTimer() {
    // Attempt monotonic clock per Phase2-M07
    const hasPerformance = typeof performance !== "undefined" && typeof performance.now === "function";
    const clockSource = hasPerformance ? "performance.now" : "date.now_fallback";
    const revealedAt = hasPerformance ? performance.now() : Date.now();
    
    return {
        client_clock_source: clockSource,
        letter_revealed_at_client_ms: revealedAt,
        client_epoch_revealed_at_ms: Date.now()
    };
}

export function stopRoundTimer(timerState) {
    const isPerf = timerState.client_clock_source === "performance.now";
    const answeredAt = isPerf ? performance.now() : Date.now();
    const elapsedMs = answeredAt - timerState.letter_revealed_at_client_ms;
    
    return {
        ...timerState,
        answer_detected_at_client_ms: answeredAt,
        elapsed_ms: elapsedMs,
        timing_pass: elapsedMs <= 3000,
        client_epoch_answered_at_ms: Date.now()
    };
}
