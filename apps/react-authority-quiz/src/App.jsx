import React, { useState } from 'react';
import PressureBackdrop from './components/PressureBackdrop';
import QuestionLadder from './components/QuestionLadder';
import ResultThresholdPanel from './components/ResultThresholdPanel';

function App() {
  const [level, setLevel] = useState(1);
  const [complete, setComplete] = useState(false);

  return (
    <PressureBackdrop level={level}>
      <div className="quiz-container">
        {!complete ? (
          <QuestionLadder level={level} onAdvance={() => setLevel(level + 1)} onComplete={() => setComplete(true)} />
        ) : (
          <ResultThresholdPanel level={level} />
        )}
      </div>
    </PressureBackdrop>
  );
}

export default App;
