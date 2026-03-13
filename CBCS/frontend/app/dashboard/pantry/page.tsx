'use client';

import { useState } from 'react';
import { Upload, Plus, Tag } from 'lucide-react';

export default function PantryPage() {
    const [rituals, setRituals] = useState([
        { id: 1, name: 'Morning Breathwork', level: 'Micro', identity: ['Seeker'], goal: 'Anxiety' },
        { id: 2, name: 'Cold Shower Challenge', level: 'Heroic', identity: ['Rebel', 'Challenger'], goal: 'Energy' },
    ]);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold text-gray-800">Component Pantry</h1>
                <button
                    onClick={() => alert("Add Ritual functionality coming in Epic 7.x!")}
                    className="bg-purple-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-purple-700 transition-colors"
                >
                    <Plus size={20} />
                    Add Ritual
                </button>
            </div>

            {/* Upload Section */}
            <div
                onClick={() => alert("Upload functionality coming in Epic 7.x!")}
                className="bg-white p-8 rounded-xl shadow-sm border border-dashed border-gray-300 flex flex-col items-center justify-center text-gray-500 hover:border-purple-500 transition-colors cursor-pointer"
            >
                <Upload size={48} className="mb-4 text-gray-400" />
                <p className="text-lg font-medium">Drag & Drop Video/Audio Files</p>
                <p className="text-sm">or click to browse</p>
            </div>

            {/* Ritual List */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {rituals.map((ritual) => (
                    <div key={ritual.id} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start mb-4">
                            <h3 className="font-semibold text-lg text-gray-800">{ritual.name}</h3>
                            <span className={`px-2 py-1 rounded text-xs font-medium ${ritual.level === 'Micro' ? 'bg-green-100 text-green-700' :
                                ritual.level === 'Heroic' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
                                }`}>
                                {ritual.level}
                            </span>
                        </div>

                        <div className="space-y-2">
                            <div className="flex items-center gap-2 text-sm text-gray-600">
                                <Tag size={16} />
                                <span>{ritual.identity.join(', ')}</span>
                            </div>
                            <div className="flex items-center gap-2 text-sm text-gray-600">
                                <span className="font-medium">Goal:</span>
                                <span>{ritual.goal}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Gap Analysis Warning */}
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                <div className="flex">
                    <div className="ml-3">
                        <p className="text-sm text-yellow-700">
                            <span className="font-bold">Gap Detected:</span> You have no rituals for <strong>High Anxiety Rebels</strong>.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
