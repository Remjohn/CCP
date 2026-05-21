import React from 'react';

export default function QuestionLadder({ level, onAdvance, onComplete }) {
    const handleAnswer = (correct) => {
        if (correct && level < 5) {
            onAdvance();
        } else {
            onComplete();
        }
    };

    return (
        <div className="ladder-card">
            <div className="level-badge">Level {level}</div>
            <h2>What is the authority question?</h2>
            <div className="options">
                <button onClick={() => handleAnswer(true)}>Correct Answer</button>
                <button onClick={() => handleAnswer(false)}>Wrong Answer</button>
            </div>
        </div>
    );
}
