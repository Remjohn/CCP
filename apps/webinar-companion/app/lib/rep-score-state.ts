export function evaluateNextSlideLock(scorecard: any | null): boolean {
    if (!scorecard) return true; // locked
    return false; // unlocked after delivery
}
