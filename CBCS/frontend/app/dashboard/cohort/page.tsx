'use client';

import { useState, useEffect } from 'react';
import { Users, Filter, Loader2 } from 'lucide-react';

interface Vibe {
    word: string;
    count: number;
    sentiment: string;
}

export default function CohortPage() {
    const [vibes, setVibes] = useState<Vibe[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedVibe, setSelectedVibe] = useState<string | null>(null);

    useEffect(() => {
        const fetchVibes = async () => {
            try {
                const res = await fetch('http://127.0.0.1:8000/api/v1/analytics/cohort-vibe');
                if (res.ok) {
                    const data = await res.json();
                    setVibes(data);
                }
            } catch (error) {
                console.error("Failed to fetch vibes:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchVibes();
    }, []);

    // Calculate max count for scaling
    const maxCount = Math.max(...vibes.map(v => v.count), 1); // Avoid div by zero

    if (loading) {
        return (
            <div className="flex h-96 items-center justify-center">
                <Loader2 className="animate-spin text-purple-600" size={48} />
            </div>
        );
    }

    return (
        <div className="space-y-8">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold text-gray-800">Cohort Vibe</h1>
                <div className="flex items-center gap-2 text-gray-500">
                    <Users size={20} />
                    <span>Active Members: 24</span>
                </div>
            </div>

            {/* Word Cloud Container */}
            <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 min-h-[400px] flex flex-wrap items-center justify-center gap-4 content-center">
                {vibes.length === 0 ? (
                    <p className="text-gray-500">No data available yet.</p>
                ) : (
                    vibes.map((vibe) => {
                        // Scale font size between 1rem and 4rem
                        const fontSize = `${1 + (vibe.count / maxCount) * 3}rem`;
                        const opacity = 0.6 + (vibe.count / maxCount) * 0.4;

                        return (
                            <button
                                key={vibe.word}
                                onClick={() => setSelectedVibe(vibe.word === selectedVibe ? null : vibe.word)}
                                style={{ fontSize, opacity }}
                                className={`
                    font-bold transition-all duration-300 hover:scale-110
                    ${vibe.sentiment === 'Negative' ? 'text-red-500 hover:text-red-600' :
                                        vibe.sentiment === 'Positive' ? 'text-green-500 hover:text-green-600' :
                                            'text-blue-500 hover:text-blue-600'}
                    ${selectedVibe && selectedVibe !== vibe.word ? 'blur-sm grayscale' : ''}
                  `}
                            >
                                {vibe.word}
                            </button>
                        );
                    })
                )}
            </div>

            {/* Drill Down Section */}
            {selectedVibe && (
                <div className="bg-gray-50 p-6 rounded-xl border border-gray-200 animate-in fade-in slide-in-from-top-4">
                    <div className="flex items-center gap-2 mb-4">
                        <Filter size={20} className="text-gray-400" />
                        <h3 className="text-lg font-semibold text-gray-700">
                            Clients feeling <span className="text-purple-600">"{selectedVibe}"</span>
                        </h3>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {/* Mock User List for Drill Down (Future: Fetch real users) */}
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="bg-white p-4 rounded shadow-sm flex items-center gap-3">
                                <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-500 font-bold">
                                    U{i}
                                </div>
                                <div>
                                    <p className="font-medium text-gray-800">Anonymous User {i}</p>
                                    <p className="text-xs text-gray-500">Matched via Journal</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
