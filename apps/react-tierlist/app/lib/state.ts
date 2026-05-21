import { TierlistBoardProjection } from './types';

export interface TierlistAppState {
    sessionId: string;
    projection: TierlistBoardProjection | null;
    recording: boolean;
    showFallback: boolean;
}

export const initialTierlistState: TierlistAppState = {
    sessionId: "",
    projection: null,
    recording: false,
    showFallback: false
};
