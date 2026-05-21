import React from 'react';
import OriginalRankingCard from './original-ranking-card';
import ProposalDiffPanel from './proposal-diff-panel';

export default function ComparisonReveal() {
    return (
        <div className="layout-grid">
            <OriginalRankingCard />
            <ProposalDiffPanel />
            <div className="card">
                <h2>Defense Status</h2>
                <p>Pending background upload...</p>
            </div>
        </div>
    );
}
