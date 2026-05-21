import React from 'react';

export default function ProposalSubmitSheet({ onSubmit }: { onSubmit: () => void }) {
    return (
        <div className="card">
            <h2>Submit Proposal</h2>
            <button onClick={onSubmit}>Submit Reorder</button>
        </div>
    );
}
