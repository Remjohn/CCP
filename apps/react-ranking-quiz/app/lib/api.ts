export async function fetchSession(sessionId: string) {
    // API mock
    return { id: sessionId };
}

export async function submitProposal(sessionId: string, items: any[]) {
    // API mock
    return { success: true };
}
