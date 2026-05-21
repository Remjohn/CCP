'use client';

import React, { useState } from 'react';
import ProposalBoard from './components/proposal-board';
import OriginalRankingCard from './components/original-ranking-card';
import ProposalSubmitSheet from './components/proposal-submit-sheet';
import ComparisonReveal from './components/comparison-reveal';

export default function Page() {
  const [submitted, setSubmitted] = useState(false);

  return (
    <main className="container">
      <header>
        <h1>Ranking Quiz</h1>
      </header>
      
      {!submitted ? (
        <div className="layout-grid">
          <OriginalRankingCard />
          <ProposalBoard />
          <ProposalSubmitSheet onSubmit={() => setSubmitted(true)} />
        </div>
      ) : (
        <ComparisonReveal />
      )}
    </main>
  );
}
