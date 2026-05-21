import React from 'react';

export default function SpeechCommandChip({ phrase }: { phrase: string }) {
    return <div className="px-3 py-1 bg-green-900 text-green-300 rounded-full text-sm inline-block">{phrase}</div>;
}
