import { TierlistMoveEvent, TierLabel } from './types';

export function interpretSpeechCommand(phrase: string, availableItems: {id: string, name: string}[]): TierlistMoveEvent | null {
    // Basic stub matching e.g. "Item 1 goes in S Tier"
    const lowerPhrase = phrase.toLowerCase();
    
    let matchedItem = null;
    for (const item of availableItems) {
        if (lowerPhrase.includes(item.name.toLowerCase())) {
            matchedItem = item;
            break;
        }
    }

    if (!matchedItem) return null;

    let targetTier: TierLabel | null = null;
    const tiers: TierLabel[] = ["S", "A", "B", "C", "D", "F"];
    for (const t of tiers) {
        if (lowerPhrase.includes(`${t.toLowerCase()} tier`) || lowerPhrase.includes(`${t.toLowerCase()} row`)) {
            targetTier = t;
            break;
        }
    }

    if (!targetTier) return null;

    // Reject low confidence (mocked by requiring exact parsing)
    if (!matchedItem || !targetTier) return null;

    return {
        event_id: Math.random().toString(),
        item_id: matchedItem.id,
        spoken_phrase: phrase,
        target_tier: targetTier,
        target_rank_index: 0,
        confidence: 0.95,
        created_at: new Date().toISOString(),
        source: "speech"
    };
}
