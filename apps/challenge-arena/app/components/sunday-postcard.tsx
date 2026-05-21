import React from 'react';

export default function SundayPostcard({ data }: { data: any }) {
  return (
    <div className="card" style={{ border: '2px solid #38bdf8' }}>
      <h3>Sunday Reflection</h3>
      <div style={{ display: 'flex', gap: '1rem', margin: '1rem 0' }}>
        <div>Sessions: {data?.sessions_completed}</div>
        <div>Words: {data?.cumulative_words_spoken}</div>
        <div>Delta: {data?.delta_words_spoken}</div>
      </div>
      <p>{data?.qualitative_interpretation}</p>
      <p style={{ fontStyle: 'italic' }}>{data?.forward_forecast}</p>
    </div>
  );
}
