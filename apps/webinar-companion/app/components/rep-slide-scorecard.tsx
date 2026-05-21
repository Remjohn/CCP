import React from 'react';
import { Scorecard } from '../lib/types';

export default function RepSlideScorecard({ data }: { data: Scorecard }) {
    return (
        <div className="rep-scorecard">
            <h3>Slide Feedback</h3>
            <p>Hedge Density: {data.hedgeDensity}</p>
            <p>Pause Architecture: {data.pauseArchitectureScore}</p>
            <p>CTA Pressure: {data.ctaPressureStability}</p>
            <p>Summary: {data.feedbackSummary}</p>
        </div>
    );
}
