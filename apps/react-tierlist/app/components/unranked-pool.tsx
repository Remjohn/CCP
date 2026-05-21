import React from 'react';
import { TierlistItem } from '../lib/types';

export default function UnrankedPool({ items }: { items: TierlistItem[] }) {
    return (
        <div className="p-4 bg-slate-800 rounded mt-4">
            <h3 className="text-sm text-slate-400 mb-2">Unranked</h3>
            <div className="flex gap-2 flex-wrap">
                {items.map(item => (
                    <div key={item.item_id} className="p-2 bg-slate-600 rounded">
                        {item.label}
                    </div>
                ))}
            </div>
        </div>
    );
}
