import React from 'react';

export default function RevealCard({ text, isHidden }) {
    if (isHidden) {
        return <div className="reveal-card hidden-card">???</div>;
    }
    
    return (
        <div className="reveal-card visible-card">
            <h3>{text}</h3>
        </div>
    );
}
