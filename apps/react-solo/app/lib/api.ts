import { SoloTopicBriefView, SoloDeploymentProjection } from './types';

export async function fetchNextTopic(coachId: string): Promise<SoloTopicBriefView> {
    // Mock API call
    return {
        id: "topic-1",
        startapp: "react_solo",
        min_duration_seconds: 120,
        max_duration_seconds: 300,
        briefing_audio_required: true,
        expires_in_seconds: 3600,
        expires_at: new Date(Date.now() + 3600000).toISOString(),
        source_label: "Source URL"
    };
}

export async function approveArtifact(artifactId: string): Promise<SoloDeploymentProjection> {
    // Mock API call
    return {
        artifact_id: artifactId,
        decision: "deployed_to_cmf",
        queue_status: "queued",
        delivery_eta_minutes: 20
    };
}
