import { DebateStance } from './types';

export interface DebateAppState {
    debateId: string;
    sourceArtifactId: string;
    selectedStance: DebateStance | null;
    phase: "lane_brief" | "stance_selection" | "recording" | "scoring" | "vs_projection";
}

export const initialDebateState: DebateAppState = {
    debateId: "",
    sourceArtifactId: "",
    selectedStance: null,
    phase: "lane_brief"
};
