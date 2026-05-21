export function saveEliminationJournal(sessionId, narrativeArc) {
    localStorage.setItem(`elimination_journal_${sessionId}`, JSON.stringify(narrativeArc));
}

export function loadEliminationJournal(sessionId) {
    const raw = localStorage.getItem(`elimination_journal_${sessionId}`);
    return raw ? JSON.parse(raw) : null;
}
