import React from 'react';

export default function ProposalDiffPanel() {
    return (
        <div className="card">
            <h2>Diff Summary</h2>
            <div className="diff-entry">
                <span>Concept A</span>
                <span>Original: 1 -> Proposed: 3 (Delta: -2)</span>
            </div>
        </div>
    );
}
