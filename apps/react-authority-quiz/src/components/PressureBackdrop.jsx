import React from 'react';

export default function PressureBackdrop({ level, children }) {
    return (
        <div className="pressure-backdrop" data-level={level}>
            {children}
        </div>
    );
}
