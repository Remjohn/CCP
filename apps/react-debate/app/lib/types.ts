export type DebateStance = "for" | "against";

export interface DebateLaunchPayload {
    startapp: "react_debate";
    debate_id: string;
    lane_key: string;
    lane_title: string;
    source_artifact_id: string;
    allowed_stances: DebateStance[];
    neutral_allowed: false;
    latest_tally_for: number;
    latest_tally_against: number;
}

export interface DebateCounterTakeIntent {
    debate_id: string;
    source_artifact_id: string;
    selected_stance: DebateStance;
    must_select_before_recording: true;
}

export interface VoteThenReactPrompt {
    prompt_id: string;
    selected_stance: DebateStance;
    prompt_copy: string;
    deep_link_url: string;
}

export interface DebateVsArtifactProjection {
    debate_id: string;
    render_format: "split_screen_vs";
    tally_for: number;
    tally_against: number;
    visual_adversary_passed: boolean;
}
