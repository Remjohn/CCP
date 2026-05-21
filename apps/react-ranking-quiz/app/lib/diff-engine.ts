export function computeDiff(originalItems: any[], proposedItems: any[]) {
    const diffs = [];
    for (let i = 0; i < proposedItems.length; i++) {
        const item = proposedItems[i];
        const origIndex = originalItems.findIndex(o => o.id === item.id);
        if (origIndex !== i) {
            diffs.push({
                itemId: item.id,
                label: item.label,
                originalSlot: origIndex,
                proposedSlot: i,
                slotDelta: origIndex - i
            });
        }
    }
    return diffs;
}
