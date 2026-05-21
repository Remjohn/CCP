export type SoloUiPhase = "brief" | "recording" | "scoring" | "score_reveal" | "deployed" | "redemption";

export interface SoloTopicBriefView {
    id: str;
    startapp: "react_solo";
    min_duration_seconds: number;
    max_duration_seconds: number;
    briefing_audio_required: boolean;
    expires_in_seconds: number;
    expires_at: string;
    source_label: string;
}

export interface SoloRecordingViewState {
    phase: SoloUiPhase;
    elapsed_seconds: number;
    max_duration_seconds: number;
    upload_ticket: string;
    upload_status: "not_started" | "pending_background" | "uploading" | "uploaded" | "failed_retryable";
    stream_status: "connected" | "degraded" | "recovered";
}

export interface SoloScoreRevealPayload {
    export_eligible: boolean;
    approval_required: boolean;
    coaching_cues: string[];
}

export interface SoloDeploymentProjection {
    artifact_id: string;
    decision: "deployed_to_cmf" | "pending_cmf_retry" | "redemption_required";
    queue_status: "not_queued" | "queued" | "delivered" | "failed_retryable";
    delivery_eta_minutes?: number;
}
