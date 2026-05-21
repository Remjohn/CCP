import React from 'react';
import { SoloScoreRevealPayload } from '../lib/types';

export default function ScoreRevealScreen({ payload }: { payload: SoloScoreRevealPayload }) {
    return (
        <div>
            <h2>Score Reveal</h2>
            <p>Eligible for Export: {payload.export_eligible ? 'Yes' : 'No'}</p>
        </div>
    );
}
