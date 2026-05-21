import React, { useState } from 'react';
import { DebateStance } from '../lib/types';

export default function StanceSelectionGate({ onSelectStance }: { onSelectStance: (stance: DebateStance) => void }) {
    const [selectedStance, setSelectedStance] = useState<DebateStance | null>(null);

    const handleConfirm = () => {
        if (selectedStance) {
            onSelectStance(selectedStance);
        }
    };

    return (
        <div>
            <h2>Choose Your Stance</h2>
            <button onClick={() => setSelectedStance('for')}>For</button>
            <button onClick={() => setSelectedStance('against')}>Against</button>
            <button onClick={handleConfirm} disabled={!selectedStance}>Confirm</button>
        </div>
    );
}
