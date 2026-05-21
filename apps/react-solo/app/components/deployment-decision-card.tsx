import React from 'react';
import { SoloScoreRevealPayload, SoloDeploymentProjection } from '../lib/types';
import { approveArtifact } from '../lib/api';

export default function DeploymentDecisionCard({ payload, artifactId }: { payload: SoloScoreRevealPayload, artifactId: string }) {
    const [projection, setProjection] = React.useState<SoloDeploymentProjection | null>(null);

    const handleApprove = async () => {
        const result = await approveArtifact(artifactId);
        setProjection(result);
    };

    if (projection) {
        if (projection.decision === 'redemption_required') {
            return <div>Redirecting to Redemption...</div>;
        }
        return <div>Status: {projection.queue_status}</div>;
    }

    return (
        <div>
            {payload.approval_required && (
                <button onClick={handleApprove}>Approve for Deployment</button>
            )}
            {!payload.export_eligible && (
                <div>Redemption required</div>
            )}
        </div>
    );
}
