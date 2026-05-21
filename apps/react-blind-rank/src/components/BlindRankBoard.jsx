import React from 'react';
import RevealCard from './RevealCard';
import DefenseRecordPanel from './DefenseRecordPanel';

export default function BlindRankBoard() {
    return (
        <div className="board">
            <h2>Blind Rank</h2>
            <div className="slots">
                <div className="slot">1. <RevealCard isHidden={false} text="Visible Item" /></div>
                <div className="slot">2. <div className="empty-slot"></div></div>
                <div className="slot">3. <div className="empty-slot"></div></div>
                <div className="slot">4. <div className="empty-slot"></div></div>
                <div className="slot">5. <div className="empty-slot"></div></div>
            </div>
            <DefenseRecordPanel />
        </div>
    );
}
