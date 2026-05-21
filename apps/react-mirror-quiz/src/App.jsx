import React, { useState } from 'react';
import MirrorQuestionCard from './components/MirrorQuestionCard';
import AudienceEvidenceDrawer from './components/AudienceEvidenceDrawer';
import RecordAnswerPanel from './components/RecordAnswerPanel';

function App() {
  const [recording, setRecording] = useState(false);

  return (
    <div className="mirror-quiz-container">
      <MirrorQuestionCard text="How do you resolve this tension?" />
      <AudienceEvidenceDrawer verbatim="I am tired of sounding smart but not converting" />
      <RecordAnswerPanel isRecording={recording} onRecordToggle={() => setRecording(!recording)} />
    </div>
  );
}

export default App;
