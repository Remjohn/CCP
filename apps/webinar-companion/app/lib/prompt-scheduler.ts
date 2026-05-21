import { PromptAnchor } from './types';

export function getActivePrompt(anchors: PromptAnchor[], currentTime: number): PromptAnchor | null {
    for (const anchor of anchors) {
        if (currentTime >= anchor.triggerAtSeconds && currentTime <= anchor.triggerAtSeconds + 30) {
            return anchor;
        }
    }
    return null;
}
