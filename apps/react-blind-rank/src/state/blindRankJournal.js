export function saveJournalState(sessionId, assignments) {
    localStorage.setItem(`br_journal_${sessionId}`, JSON.stringify(assignments));
}

export function loadJournalState(sessionId) {
    const raw = localStorage.getItem(`br_journal_${sessionId}`);
    return raw ? JSON.parse(raw) : null;
}
