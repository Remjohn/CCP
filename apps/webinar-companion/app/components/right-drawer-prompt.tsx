import React from 'react';

export default function RightDrawerPrompt({ onClose }: { onClose: () => void }) {
    return (
        <div className="right-drawer-prompt">
            <p>Right Drawer Prompt</p>
            <button onClick={onClose}>Close</button>
        </div>
    );
}
