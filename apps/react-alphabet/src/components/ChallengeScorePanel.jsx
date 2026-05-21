import React from 'react';

export default function ChallengeScorePanel() {
    return (
        <div className="score-panel">
            <h2>Challenge Complete</h2>
            <div className="status-grid">
                <div>Timing Pass: 5/5</div>
                <div>Semantic Valid: 4/5</div>
            </div>
        </div>
    );
}
