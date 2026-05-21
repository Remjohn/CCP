import React, { useEffect, useState } from 'react';
import { startRoundTimer, stopRoundTimer } from '../state/alphabetRoundTimer';

export default function LetterPromptCard({ letter, category, onComplete }) {
    const [timerState, setTimerState] = useState(null);

    useEffect(() => {
        setTimerState(startRoundTimer());
    }, [letter]);

    const handleAnswerSimulate = () => {
        if (timerState) {
            const result = stopRoundTimer(timerState);
            console.log("Timing result:", result);
            onComplete();
        }
    };

    return (
        <div className="prompt-card">
            <div className="category-label">{category}</div>
            <div className="letter-display">{letter}</div>
            <button onClick={handleAnswerSimulate} className="btn-answer">Simulate Answer Detected</button>
        </div>
    );
}
