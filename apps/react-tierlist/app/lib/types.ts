export type TierLabel = "S" | "A" | "B" | "C" | "D" | "F";

export interface TierlistItem {
    item_id: string;
    label: string;
    asset_url?: string;
    current_tier?: TierLabel;
    current_rank_index?: number;
}

export interface TierlistMoveEvent {
    event_id: string;
    item_id: string;
    spoken_phrase: string;
    target_tier: TierLabel;
    target_rank_index: number;
    confidence: number;
    created_at: string;
    source: "speech" | "manual_fallback";
}

export interface TierlistBoardProjection {
    startapp: "react_tierlist";
    topic_id: string;
    tiers: TierLabel[];
    ranked_items: TierlistItem[];
    unranked_items: TierlistItem[];
    move_events: TierlistMoveEvent[];
    snap_animation_enabled: boolean;
    speech_degraded: boolean;
}
