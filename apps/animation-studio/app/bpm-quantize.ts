// =============================================================================
// FR-VID-13 §4 Stage 3 — BPM Quantization
// "Quantize to BPM" action: snap animation keyframes to nearest beat subdivision.
// Spec reference: §4 Stage 3 Step 3, code sample.
// =============================================================================

import type { BoneOverrideKeyframe, QuantizeLevel, BPMAnalysisResult } from "./types";

/**
 * Quantize keyframes to the nearest beat subdivision.
 * This is the exact algorithm from FR-VID-13 §4 Stage 3 Step 3.
 *
 * @param keyframes - Array of keyframes with time in seconds
 * @param subdivisions - Array of beat subdivision timestamps in seconds
 * @param quantizeLevel - Which subdivision level to quantize to
 * @returns New array of keyframes with times snapped to nearest subdivision
 */
export function quantizeToBPM(
  keyframes: { time: number; [key: string]: unknown }[],
  subdivisions: number[],
  quantizeLevel: QuantizeLevel
): { time: number; [key: string]: unknown }[] {
  const grid = subdivisions;
  if (grid.length === 0) return keyframes;

  return keyframes.map((kf) => ({
    ...kf,
    time: grid.reduce((closest, beat) =>
      Math.abs(beat - kf.time) < Math.abs(closest - kf.time) ? beat : closest
    ),
  }));
}

/**
 * Convert frame-based bone override keyframes to time-based,
 * quantize to BPM, and convert back to frame-based.
 *
 * @param keyframes - Bone override keyframes (frame-based)
 * @param bpmData - BPM analysis result with subdivision timestamps
 * @param fps - Frames per second (default 24)
 * @param level - Quantization level (quarter, eighth, sixteenth)
 * @returns Quantized keyframes in frame-based format
 */
export function quantizeBoneKeyframesToBPM(
  keyframes: BoneOverrideKeyframe[],
  bpmData: BPMAnalysisResult,
  fps: number = 24,
  level: QuantizeLevel = "quarter"
): BoneOverrideKeyframe[] {
  const subdivisions = bpmData.subdivisions[level];
  if (!subdivisions || subdivisions.length === 0) return keyframes;

  // Convert frames to time in seconds
  const timeBasedKeyframes = keyframes.map((kf) => ({
    ...kf,
    time: kf.frame / fps,
  }));

  // Quantize
  const quantized = quantizeToBPM(timeBasedKeyframes, subdivisions, level);

  // Convert back to frames
  return quantized.map((kf) => ({
    frame: Math.round(kf.time * fps),
    rotation: kf.rotation as number | undefined,
    x: kf.x as number | undefined,
    y: kf.y as number | undefined,
    scaleX: kf.scaleX as number | undefined,
    scaleY: kf.scaleY as number | undefined,
  }));
}

/**
 * Calculate beat grid timestamps from BPM for timeline rendering.
 *
 * @param bpm - Beats per minute
 * @param durationSec - Total duration in seconds
 * @param level - Subdivision level
 * @returns Array of timestamps in seconds for grid lines
 */
export function calculateBeatGrid(
  bpm: number,
  durationSec: number,
  level: QuantizeLevel = "quarter"
): number[] {
  if (bpm <= 0 || durationSec <= 0) return [];

  const beatDuration = 60 / bpm;
  let subdivisionDuration: number;

  switch (level) {
    case "quarter":
      subdivisionDuration = beatDuration;
      break;
    case "eighth":
      subdivisionDuration = beatDuration / 2;
      break;
    case "sixteenth":
      subdivisionDuration = beatDuration / 4;
      break;
  }

  const timestamps: number[] = [];
  let t = 0;
  while (t <= durationSec) {
    timestamps.push(Math.round(t * 1000) / 1000); // Round to ms precision
    t += subdivisionDuration;
  }

  return timestamps;
}
