import React, { useState } from 'react';
import EliminationBoard from './components/EliminationBoard';
import SurvivorRevealPanel from './components/SurvivorRevealPanel';

function App() {
  const [ladderComplete, setLadderComplete] = useState(false);

  return (
    <div className="elimination-container">
      {!ladderComplete ? (
        <EliminationBoard onComplete={() => setLadderComplete(true)} />
      ) : (
        <SurvivorRevealPanel />
      )}
    </div>
  );
}

export default App;
