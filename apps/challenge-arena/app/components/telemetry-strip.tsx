import React from 'react';

export default function TelemetryStrip() {
  return (
    <div className="card" style={{ marginTop: '2rem', display: 'flex', justifyContent: 'space-around' }}>
      <div>
        <h4>Completed</h4>
        <p>4 Sessions</p>
      </div>
      <div>
        <h4>Words Spoken</h4>
        <p>1,245</p>
      </div>
      <div>
        <h4>Hedge Frequency</h4>
        <p>1.2 / min</p>
      </div>
    </div>
  );
}
