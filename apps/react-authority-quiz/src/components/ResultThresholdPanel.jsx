import React from 'react';

export default function ResultThresholdPanel({ level }) {
    return (
        <div className="result-panel">
            <h2>Quiz Complete</h2>
            <p>You reached Level {level}</p>
        </div>
    );
}
