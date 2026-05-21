import React from 'react';
import { SoloRecordingViewState } from '../lib/types';

export default function RecordingConsole({ state }: { state: SoloRecordingViewState }) {
    return (
        <div className="recording-console">
            <h2>Recording...</h2>
            <p>Time: {state.elapsed_seconds}s</p>
            <button onClick={() => console.log("Finalize")}>Stop & Finalize</button>
        </div>
    );
}
