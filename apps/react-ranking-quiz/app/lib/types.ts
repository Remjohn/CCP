export interface RankingItem {
    id: str;
    label: str;
}

export interface DiffEntry {
    itemId: str;
    label: str;
    originalSlot: number;
    proposedSlot: number;
    slotDelta: number;
}
