import React from 'react';

export default function DraggableRankingItem({ label }: { label: string }) {
    return (
        <div className="board-item">{label}</div>
    );
}
