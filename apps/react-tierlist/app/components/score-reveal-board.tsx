import React from 'react';
import TierlistBoard from './tierlist-board';

export default function ScoreRevealBoard() {
    return (
        <div className="p-4 border-2 border-green-500 rounded">
            <h2 className="text-xl font-bold mb-4 text-green-400">Final Tierlist</h2>
            <TierlistBoard />
        </div>
    );
}
