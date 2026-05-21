import React, { useState } from 'react';
import LetterPromptCard from './components/LetterPromptCard';
import RoundProgressRail from './components/RoundProgressRail';
import ChallengeScorePanel from './components/ChallengeScorePanel';

function App() {
  const [roundComplete, setRoundComplete] = useState(false);

  return (
    <div className="alphabet-container">
      <RoundProgressRail />
      {!roundComplete ? (
        <LetterPromptCard letter="A" category="Industry Terms" onComplete={() => setRoundComplete(true)} />
      ) : (
        <ChallengeScorePanel />
      )}
    </div>
  );
}

export default App;
