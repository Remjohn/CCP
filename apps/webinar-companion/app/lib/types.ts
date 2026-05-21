export interface VideoRect {
    x: number;
    y: number;
    width: number;
    height: number;
}

export interface PromptAnchor {
    promptId: string;
    triggerAtSeconds: number;
    promptType: 'poll' | 'voice_note' | 'reaction' | 'cta';
    preferredGeometry: 'lower_third' | 'right_drawer';
}

export interface Scorecard {
    hedgeDensity: number;
    pauseArchitectureScore: number;
    ctaPressureStability: number;
    feedbackSummary: string;
}
