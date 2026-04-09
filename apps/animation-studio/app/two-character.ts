// =============================================================================
// FR-VID-13 §8 Task 17 — Two-Character Interaction Support
// Shared coordinate space for coach + client avatars.
// =============================================================================

import type { CharacterPackage, SceneId, TargetFormat } from "./types";
import { computeSceneTransform } from "./scene-presets";

/**
 * Two-character interaction slot assignments.
 * In a two-character scene, each character occupies a defined slot
 * within the shared coordinate space.
 */
export type CharacterSlot = "primary" | "secondary";

export interface TwoCharacterLayout {
  primary: { x: number; y: number; scale: number; flipX: boolean };
  secondary: { x: number; y: number; scale: number; flipX: boolean };
}

/**
 * Scene presets adapted for two-character interactions.
 * The primary character (coach) occupies the dominant position.
 * The secondary character (client) occupies the response position.
 */
const TWO_CHAR_LAYOUTS: Record<SceneId, Record<TargetFormat, TwoCharacterLayout>> = {
  "SC-01": {
    "9:16": {
      primary:   { x: 0.35, y: 0.6, scale: 0.5, flipX: false },
      secondary: { x: 0.65, y: 0.6, scale: 0.45, flipX: true },
    },
    "1:1": {
      primary:   { x: 0.3, y: 0.55, scale: 0.45, flipX: false },
      secondary: { x: 0.7, y: 0.55, scale: 0.4, flipX: true },
    },
    "16:9": {
      primary:   { x: 0.3, y: 0.65, scale: 0.4, flipX: false },
      secondary: { x: 0.7, y: 0.65, scale: 0.35, flipX: true },
    },
    "4:5": {
      primary:   { x: 0.33, y: 0.6, scale: 0.48, flipX: false },
      secondary: { x: 0.67, y: 0.6, scale: 0.43, flipX: true },
    },
  },
  // SC-03 (Split) is particularly suited for two characters
  "SC-03": {
    "9:16": {
      primary:   { x: 0.3, y: 0.5, scale: 0.45, flipX: false },
      secondary: { x: 0.7, y: 0.5, scale: 0.45, flipX: true },
    },
    "1:1": {
      primary:   { x: 0.25, y: 0.5, scale: 0.4, flipX: false },
      secondary: { x: 0.75, y: 0.5, scale: 0.4, flipX: true },
    },
    "16:9": {
      primary:   { x: 0.25, y: 0.5, scale: 0.35, flipX: false },
      secondary: { x: 0.75, y: 0.5, scale: 0.35, flipX: true },
    },
    "4:5": {
      primary:   { x: 0.28, y: 0.5, scale: 0.42, flipX: false },
      secondary: { x: 0.72, y: 0.5, scale: 0.42, flipX: true },
    },
  },
  // Remaining scenes use default split layout
  "SC-02": { "9:16": { primary: { x: 0.35, y: 0.6, scale: 0.5, flipX: false }, secondary: { x: 0.65, y: 0.6, scale: 0.3, flipX: true } }, "1:1": { primary: { x: 0.35, y: 0.55, scale: 0.45, flipX: false }, secondary: { x: 0.65, y: 0.55, scale: 0.28, flipX: true } }, "16:9": { primary: { x: 0.35, y: 0.65, scale: 0.4, flipX: false }, secondary: { x: 0.65, y: 0.65, scale: 0.25, flipX: true } }, "4:5": { primary: { x: 0.35, y: 0.6, scale: 0.48, flipX: false }, secondary: { x: 0.65, y: 0.6, scale: 0.3, flipX: true } } },
  "SC-04": { "9:16": { primary: { x: 0.35, y: 0.5, scale: 0.45, flipX: false }, secondary: { x: 0.7, y: 0.5, scale: 0.35, flipX: true } }, "1:1": { primary: { x: 0.35, y: 0.5, scale: 0.4, flipX: false }, secondary: { x: 0.7, y: 0.5, scale: 0.33, flipX: true } }, "16:9": { primary: { x: 0.3, y: 0.5, scale: 0.35, flipX: false }, secondary: { x: 0.7, y: 0.5, scale: 0.3, flipX: true } }, "4:5": { primary: { x: 0.35, y: 0.5, scale: 0.42, flipX: false }, secondary: { x: 0.7, y: 0.5, scale: 0.34, flipX: true } } },
  "SC-05": { "9:16": { primary: { x: 0.35, y: 0.5, scale: 0.65, flipX: false }, secondary: { x: 0.65, y: 0.5, scale: 0.6, flipX: true } }, "1:1": { primary: { x: 0.35, y: 0.48, scale: 0.6, flipX: false }, secondary: { x: 0.65, y: 0.48, scale: 0.55, flipX: true } }, "16:9": { primary: { x: 0.35, y: 0.5, scale: 0.5, flipX: false }, secondary: { x: 0.65, y: 0.5, scale: 0.45, flipX: true } }, "4:5": { primary: { x: 0.35, y: 0.5, scale: 0.63, flipX: false }, secondary: { x: 0.65, y: 0.5, scale: 0.58, flipX: true } } },
  "SC-06": { "9:16": { primary: { x: 0.35, y: 0.4, scale: 1.0, flipX: false }, secondary: { x: 0.65, y: 0.4, scale: 0.9, flipX: true } }, "1:1": { primary: { x: 0.35, y: 0.38, scale: 0.9, flipX: false }, secondary: { x: 0.65, y: 0.38, scale: 0.8, flipX: true } }, "16:9": { primary: { x: 0.35, y: 0.4, scale: 0.8, flipX: false }, secondary: { x: 0.65, y: 0.4, scale: 0.7, flipX: true } }, "4:5": { primary: { x: 0.35, y: 0.4, scale: 0.95, flipX: false }, secondary: { x: 0.65, y: 0.4, scale: 0.85, flipX: true } } },
  "SC-07": { "9:16": { primary: { x: 0.75, y: 0.15, scale: 0.18, flipX: false }, secondary: { x: 0.25, y: 0.85, scale: 0.18, flipX: true } }, "1:1": { primary: { x: 0.75, y: 0.15, scale: 0.16, flipX: false }, secondary: { x: 0.25, y: 0.85, scale: 0.16, flipX: true } }, "16:9": { primary: { x: 0.8, y: 0.15, scale: 0.13, flipX: false }, secondary: { x: 0.2, y: 0.85, scale: 0.13, flipX: true } }, "4:5": { primary: { x: 0.75, y: 0.15, scale: 0.17, flipX: false }, secondary: { x: 0.25, y: 0.85, scale: 0.17, flipX: true } } },
  "SC-08": { "9:16": { primary: { x: -0.2, y: 0.5, scale: 0.5, flipX: false }, secondary: { x: 1.2, y: 0.5, scale: 0.5, flipX: true } }, "1:1": { primary: { x: -0.2, y: 0.5, scale: 0.5, flipX: false }, secondary: { x: 1.2, y: 0.5, scale: 0.5, flipX: true } }, "16:9": { primary: { x: -0.2, y: 0.5, scale: 0.5, flipX: false }, secondary: { x: 1.2, y: 0.5, scale: 0.5, flipX: true } }, "4:5": { primary: { x: -0.2, y: 0.5, scale: 0.5, flipX: false }, secondary: { x: 1.2, y: 0.5, scale: 0.5, flipX: true } } },
};

/**
 * Compute pixel positions for a two-character scene.
 *
 * @param sceneId - Scene preset ID
 * @param format - Target format
 * @param primaryCharWidth - Primary character base width
 * @param primaryCharHeight - Primary character base height
 * @param secondaryCharWidth - Secondary character base width
 * @param secondaryCharHeight - Secondary character base height
 * @returns Transform data for both characters in pixel space
 */
export function computeTwoCharacterTransform(
  sceneId: SceneId,
  format: TargetFormat,
  primaryCharWidth: number,
  primaryCharHeight: number,
  secondaryCharWidth: number,
  secondaryCharHeight: number
): {
  primary: { x: number; y: number; scale: number; flipX: boolean };
  secondary: { x: number; y: number; scale: number; flipX: boolean };
} {
  const layout = TWO_CHAR_LAYOUTS[sceneId]?.[format];
  if (!layout) {
    // Fallback to SC-01
    return computeTwoCharacterTransform("SC-01", format, primaryCharWidth, primaryCharHeight, secondaryCharWidth, secondaryCharHeight);
  }

  const dims = {
    "9:16": { width: 1080, height: 1920 },
    "1:1": { width: 1080, height: 1080 },
    "16:9": { width: 1920, height: 1080 },
    "4:5": { width: 1080, height: 1350 },
  }[format];

  return {
    primary: {
      x: layout.primary.x * dims.width,
      y: layout.primary.y * dims.height,
      scale: layout.primary.scale * (dims.width / primaryCharWidth),
      flipX: layout.primary.flipX,
    },
    secondary: {
      x: layout.secondary.x * dims.width,
      y: layout.secondary.y * dims.height,
      scale: layout.secondary.scale * (dims.width / secondaryCharWidth),
      flipX: layout.secondary.flipX,
    },
  };
}
