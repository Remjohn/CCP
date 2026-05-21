import React, { useState } from 'react';
import RoundTimer from './RoundTimer';

export default function EliminationBoard({ onComplete }) {
    const [options, setOptions] = useState([
        { id: '1', text: 'Option 1' },
        { id: '2', text: 'Option 2' },
        { id: '3', text: 'Option 3' },
        { id: '4', text: 'Option 4' },
        { id: '5', text: 'Option 5' },
        { id: '6', text: 'Option 6' },
        { id: '7', text: 'Option 7' },
        { id: '8', text: 'Option 8' }
    ]);
    
    const [activeCount, setActiveCount] = useState(8);

    const handleEliminate = (id) => {
        setOptions(options.filter(o => o.id !== id));
        const newCount = activeCount - 1;
        setActiveCount(newCount);
        if (newCount === 1) {
            onComplete();
        }
    };

    return (
        <div className="board">
            <h2>Last One Standing</h2>
            <RoundTimer activeCount={activeCount} />
            <div className="options-grid">
                {options.map(o => (
                    <button 
                        key={o.id} 
                        className="btn-option" 
                        onDoubleClick={() => handleEliminate(o.id)}
                    >
                        {o.text} (Double Tap to Eliminate)
                    </button>
                ))}
            </div>
        </div>
    );
}
