// =============================================================================
// FR-VID-13 §4 Stage 7 — Scene Composition Presets (SC-01 through SC-08 × 4 formats)
// Values from spec: {position}, {scale as % of canvas width}, {y-position as % from top}
// =============================================================================

import {
  SceneId,
  TargetFormat,
  ScenePreset,
  SceneFormatMatrix,
  FORMAT_DIMENSIONS,
} from "./types";

/**
 * Scene × Format Matrix — exact values from FR-VID-13 §4 Stage 7.
 * Each entry defines: position anchor, scale (% of canvas width), y (% from top).
 */
export const SCENE_FORMAT_MATRIX: SceneFormatMatrix = {
  "SC-01": {
    "9:16":  { position: "center",       scale_pct: 60,  y_pct: 60 },
    "1:1":   { position: "center",       scale_pct: 55,  y_pct: 55 },
    "16:9":  { position: "center",       scale_pct: 50,  y_pct: 65 },
    "4:5":   { position: "center",       scale_pct: 58,  y_pct: 60 },
  },
  "SC-02": {
    "9:16":  { position: "bottom-right", scale_pct: 35,  y_pct: 0 },
    "1:1":   { position: "bottom-right", scale_pct: 30,  y_pct: 0 },
    "16:9":  { position: "bottom-right", scale_pct: 25,  y_pct: 0 },
    "4:5":   { position: "bottom-right", scale_pct: 32,  y_pct: 0 },
  },
  "SC-03": {
    "9:16":  { position: "left",         scale_pct: 50,  y_pct: 0 },
    "1:1":   { position: "left",         scale_pct: 45,  y_pct: 0 },
    "16:9":  { position: "left",         scale_pct: 40,  y_pct: 0 },
    "4:5":   { position: "left",         scale_pct: 48,  y_pct: 0 },
  },
  "SC-04": {
    "9:16":  { position: "right",        scale_pct: 40,  y_pct: 0 },
    "1:1":   { position: "right",        scale_pct: 38,  y_pct: 0 },
    "16:9":  { position: "right",        scale_pct: 35,  y_pct: 0 },
    "4:5":   { position: "right",        scale_pct: 39,  y_pct: 0 },
  },
  "SC-05": {
    "9:16":  { position: "center",       scale_pct: 80,  y_pct: 50 },
    "1:1":   { position: "center",       scale_pct: 75,  y_pct: 48 },
    "16:9":  { position: "center",       scale_pct: 65,  y_pct: 50 },
    "4:5":   { position: "center",       scale_pct: 78,  y_pct: 50 },
  },
  "SC-06": {
    "9:16":  { position: "center",       scale_pct: 120, y_pct: 40 },
    "1:1":   { position: "center",       scale_pct: 110, y_pct: 38 },
    "16:9":  { position: "center",       scale_pct: 100, y_pct: 40 },
    "4:5":   { position: "center",       scale_pct: 115, y_pct: 40 },
  },
  "SC-07": {
    "9:16":  { position: "top-right",    scale_pct: 20,  y_pct: 0 },
    "1:1":   { position: "top-right",    scale_pct: 18,  y_pct: 0 },
    "16:9":  { position: "top-right",    scale_pct: 15,  y_pct: 0 },
    "4:5":   { position: "top-right",    scale_pct: 19,  y_pct: 0 },
  },
  "SC-08": {
    "9:16":  { position: "off-left",     scale_pct: 60,  y_pct: 0 },
    "1:1":   { position: "off-left",     scale_pct: 60,  y_pct: 0 },
    "16:9":  { position: "off-left",     scale_pct: 60,  y_pct: 0 },
    "4:5":   { position: "off-left",     scale_pct: 60,  y_pct: 0 },
  },
};

/**
 * Compute the absolute pixel position and scale for a character given a scene and format.
 * Used by both the studio canvas (Stage 7) and the headless frame export (Stage 6).
 *
 * @returns { x, y, scale } in pixels, suitable for PixiJS container transforms.
 */
export function computeSceneTransform(
  sceneId: SceneId,
  format: TargetFormat,
  characterBaseWidth: number,
  characterBaseHeight: number
): { x: number; y: number; scale: number } {
  const preset = SCENE_FORMAT_MATRIX[sceneId][format];
  const dims = FORMAT_DIMENSIONS[format];

  // Scale: character width as percentage of canvas width
  const scale = (preset.scale_pct / 100) * (dims.width / characterBaseWidth);

  // Position anchor calculation
  let x: number;
  let y: number;

  switch (preset.position) {
    case "center":
      x = dims.width / 2;
      y = (preset.y_pct / 100) * dims.height;
      break;
    case "bottom-right":
      x = dims.width * 0.8;
      y = dims.height * 0.8;
      break;
    case "left":
      x = dims.width * 0.25;
      y = dims.height * 0.5;
      break;
    case "right":
      x = dims.width * 0.75;
      y = dims.height * 0.5;
      break;
    case "top-right":
      x = dims.width * 0.85;
      y = dims.height * 0.15;
      break;
    case "off-left":
      // SC-08 Walk Entrance: starts off-screen left, settles to center
      x = -characterBaseWidth * scale;
      y = dims.height * 0.5;
      break;
    default:
      x = dims.width / 2;
      y = dims.height / 2;
  }

  return { x, y, scale };
}

/**
 * For SC-08 (Walk Entrance), compute the settle position after the entrance animation.
 * The entrance walks from off-left to center at 60% scale.
 */
export function computeSC08SettleTransform(
  format: TargetFormat,
  characterBaseWidth: number
): { x: number; y: number; scale: number } {
  const dims = FORMAT_DIMENSIONS[format];
  const scale = 0.6 * (dims.width / characterBaseWidth);
  return {
    x: dims.width / 2,
    y: dims.height * 0.5,
    scale,
  };
}
