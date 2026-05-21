import React from 'react';

export default function LowerThirdPrompt({ onClose }: { onClose: () => void }) {
    return (
        <div className="lower-third-prompt">
            <p>Lower Third Prompt</p>
            <button onClick={onClose}>Close</button>
        </div>
    );
}
