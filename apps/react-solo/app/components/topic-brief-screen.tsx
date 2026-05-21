import React from 'react';
import { fetchNextTopic } from '../lib/api';
import { SoloTopicBriefView } from '../lib/types';

export default function TopicBriefScreen() {
    const [topic, setTopic] = React.useState<SoloTopicBriefView | null>(null);

    React.useEffect(() => {
        fetchNextTopic("test").then(setTopic);
    }, []);

    if (!topic) return <div>Loading...</div>;

    const isExpired = topic.expires_in_seconds <= 0;

    return (
        <div className="p-6 max-w-sm mx-auto bg-slate-800 rounded-xl shadow-md space-y-4">
            <h1 className="text-xl font-bold">Topic Brief</h1>
            <p>Source: <a href="#">{topic.source_label}</a></p>
            <p>Expires in: {topic.expires_in_seconds}s</p>
            <button 
                disabled={isExpired}
                className={`w-full py-2 rounded ${isExpired ? 'bg-gray-500' : 'bg-blue-600'}`}
            >
                {isExpired ? 'TOPIC_EXPIRED' : 'Record Take'}
            </button>
        </div>
    );
}
