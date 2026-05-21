import { TierlistBoardProjection, TierlistMoveEvent } from './types';

export async function fetchTierlistProjection(sessionId: string): Promise<TierlistBoardProjection> {
    // Mock API
    return {
        startapp: "react_tierlist",
        topic_id: "topic-1",
        tiers: ["S", "A", "B", "C"],
        ranked_items: [],
        unranked_items: [
            { item_id: "1", label: "Item 1" },
            { item_id: "2", label: "Item 2" },
        ],
        move_events: [],
        snap_animation_enabled: true,
        speech_degraded: false
    };
}

export async function submitManualMove(sessionId: string, move: TierlistMoveEvent): Promise<void> {
    // Mock API
}
