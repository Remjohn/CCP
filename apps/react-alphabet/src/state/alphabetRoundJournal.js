export function saveRoundJournal(sessionId, roundResults) {
    localStorage.setItem(`alphabet_journal_${sessionId}`, JSON.stringify(roundResults));
}

export function loadRoundJournal(sessionId) {
    const raw = localStorage.getItem(`alphabet_journal_${sessionId}`);
    return raw ? JSON.parse(raw) : null;
}
