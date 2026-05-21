export function createEliminationMachine(options) {
    let activeOptions = [...options];
    let eliminatedOptions = [];
    
    return {
        getActive: () => activeOptions,
        getEliminated: () => eliminatedOptions,
        eliminate: (optionId) => {
            const idx = activeOptions.findIndex(o => o.id === optionId);
            if (idx > -1) {
                const [eliminated] = activeOptions.splice(idx, 1);
                eliminatedOptions.push(eliminated);
            }
        },
        isComplete: () => activeOptions.length === 1
    };
}
