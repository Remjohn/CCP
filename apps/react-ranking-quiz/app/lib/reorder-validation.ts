export function validateReorder(originalItems: any[], proposedItems: any[]) {
    if (originalItems.length !== proposedItems.length) return false;
    // ensure no missing/duplicate logic here
    return true;
}
