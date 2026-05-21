export const BlindRankStateName = {
    SESSION_READY: "session_ready",
    ITEM_REVEALED: "item_revealed",
    AWAITING_SLOT_LOCK: "awaiting_slot_lock",
    SLOT_LOCKED: "slot_locked",
    NEXT_ITEM_PENDING: "next_item_pending",
    BOARD_COMPLETE: "board_complete",
    DEFENSE_RECORDING: "defense_recording"
};

export function createMachine(initialState = BlindRankStateName.SESSION_READY) {
    let state = initialState;
    
    return {
        getState: () => state,
        transition: (action) => {
            // Mock state machine for spec validation
            if (action === 'REVEAL_FIRST_ITEM') state = BlindRankStateName.ITEM_REVEALED;
            if (action === 'LOCK_SLOT') state = BlindRankStateName.SLOT_LOCKED;
            if (action === 'REVEAL_NEXT_ITEM') state = BlindRankStateName.ITEM_REVEALED;
            if (action === 'COMPLETE_BOARD') state = BlindRankStateName.BOARD_COMPLETE;
            if (action === 'START_DEFENSE_RECORDING') state = BlindRankStateName.DEFENSE_RECORDING;
            return state;
        }
    };
}
