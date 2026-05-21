import React from 'react';

export default function RecordAnswerPanel({ isRecording, onRecordToggle }) {
  return (
    <div className="record-panel">
      <button onClick={onRecordToggle} className={isRecording ? 'btn-stop' : 'btn-start'}>
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
    </div>
  );
}
