import React from 'react';
import TierRow from './tier-row';
import UnrankedPool from './unranked-pool';

export default function TierlistBoard() {
    return (
        <div className="w-full max-w-4xl">
            <TierRow label="S" items={[]} />
            <TierRow label="A" items={[]} />
            <TierRow label="B" items={[]} />
            <TierRow label="C" items={[]} />
            <UnrankedPool items={[]} />
        </div>
    );
}
