import React from 'react';

export default function RoundTimer({ activeCount }) {
    let aggression = "calm";
    if (activeCount < 3) aggression = "final";
    else if (activeCount < 4) aggression = "intense";
    else if (activeCount < 6) aggression = "pressured";

    return (
        <div className="timer-container" data-aggression={aggression}>
            <div className="timer-bar"></div>
            <p>Aggression: {aggression}</p>
        </div>
    );
}
