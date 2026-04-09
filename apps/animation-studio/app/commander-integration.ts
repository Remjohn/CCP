// =============================================================================
// FR-VID-13 §8 Task 19 — Pipeline Commander Integration
// Adds ANIMATING state between READY_FOR_REVIEW and RENDERING_FINAL in the
// FR-VID-09 Pipeline Commander state machine.
// =============================================================================

/**
 * Extended pipeline states including the new ANIMATING state.
 * Original 16 states from FR-VID-09 + ANIMATING = 17 states.
 *
 * Flow: ... → READY_FOR_REVIEW → ANIMATING → RENDERING_FINAL → ...
 */
export const PIPELINE_STATES = {
  // Original FR-VID-09 states (16)
  IDLE: "IDLE",
  QUEUED: "QUEUED",
  INGESTING: "INGESTING",
  INGESTION_FAILED: "INGESTION_FAILED",
  GENERATING_T2I: "GENERATING_T2I",
  T2I_QUALITY_CHECK: "T2I_QUALITY_CHECK",
  GENERATING_I2V: "GENERATING_I2V",
  ASSEMBLING_MANIFEST: "ASSEMBLING_MANIFEST",
  GENERATING_CAPTIONS: "GENERATING_CAPTIONS",
  COMPOSITING: "COMPOSITING",
  READY_FOR_REVIEW: "READY_FOR_REVIEW",
  // NEW: Animation Studio state (FR-VID-13)
  ANIMATING: "ANIMATING",
  // Continue FR-VID-09 states
  RENDERING_PREVIEW: "RENDERING_PREVIEW",
  RENDERING_FINAL: "RENDERING_FINAL",
  RENDER_FAILED: "RENDER_FAILED",
  COMPLETED: "COMPLETED",
  FAILED: "FAILED",
} as const;

export type PipelineState = (typeof PIPELINE_STATES)[keyof typeof PIPELINE_STATES];

/**
 * Valid state transitions including the ANIMATING state.
 * READY_FOR_REVIEW → ANIMATING: Operator opens Animation Studio.
 * ANIMATING → RENDERING_FINAL: Operator exports manifest patch + frame export completes.
 * ANIMATING → READY_FOR_REVIEW: Operator cancels animation session (no changes saved).
 */
export const STATE_TRANSITIONS: Record<PipelineState, PipelineState[]> = {
  IDLE: ["QUEUED"],
  QUEUED: ["INGESTING", "FAILED"],
  INGESTING: ["GENERATING_T2I", "INGESTION_FAILED"],
  INGESTION_FAILED: ["QUEUED", "FAILED"],
  GENERATING_T2I: ["T2I_QUALITY_CHECK", "FAILED"],
  T2I_QUALITY_CHECK: ["GENERATING_I2V", "GENERATING_T2I", "FAILED"],
  GENERATING_I2V: ["ASSEMBLING_MANIFEST", "FAILED"],
  ASSEMBLING_MANIFEST: ["GENERATING_CAPTIONS", "FAILED"],
  GENERATING_CAPTIONS: ["COMPOSITING", "FAILED"],
  COMPOSITING: ["READY_FOR_REVIEW", "FAILED"],
  READY_FOR_REVIEW: ["ANIMATING", "RENDERING_PREVIEW", "RENDERING_FINAL", "FAILED"],
  ANIMATING: ["RENDERING_FINAL", "READY_FOR_REVIEW"],
  RENDERING_PREVIEW: ["READY_FOR_REVIEW", "RENDERING_FINAL", "RENDER_FAILED"],
  RENDERING_FINAL: ["COMPLETED", "RENDER_FAILED"],
  RENDER_FAILED: ["RENDERING_FINAL", "READY_FOR_REVIEW", "FAILED"],
  COMPLETED: ["IDLE"],
  FAILED: ["IDLE", "QUEUED"],
};

/**
 * Validate a state transition is legal.
 */
export function isValidTransition(from: PipelineState, to: PipelineState): boolean {
  const allowed = STATE_TRANSITIONS[from];
  return allowed ? allowed.includes(to) : false;
}

/**
 * Transition the pipeline to the ANIMATING state.
 * Called when the operator opens the Animation Studio from the review UI.
 *
 * @param currentState - Current pipeline state
 * @returns The new state, or throws if transition is invalid
 */
export function transitionToAnimating(currentState: PipelineState): PipelineState {
  if (currentState !== "READY_FOR_REVIEW") {
    throw new Error(
      `Cannot transition to ANIMATING from '${currentState}'. ` +
      `Must be in READY_FOR_REVIEW state.`
    );
  }
  return PIPELINE_STATES.ANIMATING;
}

/**
 * Complete the animation session and transition to RENDERING_FINAL.
 * Called after the operator exports the manifest patch and frame export completes.
 *
 * @param currentState - Current pipeline state (must be ANIMATING)
 * @param patchExported - Whether the manifest patch was exported
 * @param framesExported - Whether all frame exports completed successfully
 * @returns The new state
 */
export function completeAnimationSession(
  currentState: PipelineState,
  patchExported: boolean,
  framesExported: boolean
): PipelineState {
  if (currentState !== "ANIMATING") {
    throw new Error(
      `Cannot complete animation session from '${currentState}'. ` +
      `Must be in ANIMATING state.`
    );
  }

  if (!patchExported) {
    throw new Error("Cannot transition to RENDERING_FINAL: manifest patch not exported.");
  }

  if (!framesExported) {
    throw new Error("Cannot transition to RENDERING_FINAL: frame exports not completed.");
  }

  return PIPELINE_STATES.RENDERING_FINAL;
}

/**
 * Cancel the animation session and return to READY_FOR_REVIEW.
 * No changes are saved.
 */
export function cancelAnimationSession(currentState: PipelineState): PipelineState {
  if (currentState !== "ANIMATING") {
    throw new Error(
      `Cannot cancel animation session from '${currentState}'. ` +
      `Must be in ANIMATING state.`
    );
  }
  return PIPELINE_STATES.READY_FOR_REVIEW;
}
