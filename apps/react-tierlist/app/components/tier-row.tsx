import React from 'react';
import { TierlistItem } from '../lib/types';

export default function TierRow({ label, items }: { label: string, items: TierlistItem[] }) {
    return (
        <div className="flex border-b border-slate-700 min-h-24">
            <div className="w-16 flex items-center justify-center font-bold text-xl bg-slate-800 border-r border-slate-700">
                {label}
            </div>
            <div className="flex-1 p-2 flex gap-2 flex-wrap">
                {items.map(item => (
                    <div key={item.item_id} className="p-2 bg-blue-600 rounded">
                        {item.label}
                    </div>
                ))}
            </div>
        </div>
    );
}
