import React, { useEffect, useState } from 'react';

export default function TierSnapOverlay({ active, children }: { active: boolean, children: React.ReactNode }) {
    const [snapClass, setSnapClass] = useState("tier-snap-done");

    useEffect(() => {
        if (active) {
            setSnapClass("tier-snap-active");
            const t = setTimeout(() => setSnapClass("tier-snap-done"), 300);
            return () => clearTimeout(t);
        }
    }, [active]);

    return <div className={snapClass}>{children}</div>;
}
