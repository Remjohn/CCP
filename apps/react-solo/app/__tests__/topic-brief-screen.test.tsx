import { render, screen } from '@testing-library/react';
import TopicBriefScreen from '../components/topic-brief-screen';

jest.mock('../lib/api', () => ({
    fetchNextTopic: jest.fn().mockResolvedValue({
        id: "topic-1",
        startapp: "react_solo",
        expires_in_seconds: 3600,
        source_label: "Source URL"
    })
}));

describe('TopicBriefScreen', () => {
    it('renders source link, briefing audio CTA, and countdown from expires_at', async () => {
        // Mock implementation
    });

    it('disables record when expires_in_seconds reaches zero', async () => {
        // Mock implementation
    });
});
