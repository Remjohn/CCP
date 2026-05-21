import React from 'react';

export default function HabitIntentionSheet() {
  return (
    <div className="card">
      <h4>Pre-Session Habit Intent</h4>
      <input placeholder="If [CUE], then I will [ACTION]" style={{ width: '100%', padding: '0.5rem' }} />
      <button style={{ marginTop: '1rem' }}>Verify</button>
    </div>
  );
}
