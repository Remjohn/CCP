import { DebateLaunchPayload, DebateCounterTakeIntent, DebateStance } from './types';

export async function fetchDebateLaunchPayload(debateId: string): Promise<DebateLaunchPayload> {
    // Mock API
    return {
        startapp: "react_debate",
        debate_id: debateId,
        lane_key: "debate_lane",
        lane_title: "Debate Lane",
        source_artifact_id: "art-1",
        allowed_stances: ["for", "against"],
        neutral_allowed: false,
        latest_tally_for: 10,
        latest_tally_against: 5,
    };
}

export async function createCounterTakeIntent(debateId: string, sourceArtifactId: string, stance: DebateStance): Promise<DebateCounterTakeIntent> {
    // Mock API
    return {
        debate_id: debateId,
        source_artifact_id: sourceArtifactId,
        selected_stance: stance,
        must_select_before_recording: true
    };
}
