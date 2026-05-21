import React from 'react';

export default function JuryTallyCard({ tallyFor, tallyAgainst }: { tallyFor: number, tallyAgainst: number }) {
    return (
        <div>
            <h3>Jury Tally</h3>
            <p>For: {tallyFor}</p>
            <p>Against: {tallyAgainst}</p>
        </div>
    );
}
