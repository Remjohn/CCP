// =============================================================================
// FR-VID-13 — Receipt Chain Implementation
// §Receipt Chain: 8 stages, each emitting a receipt with hash linkage.
// =============================================================================

import { v4 as uuidv4 } from "uuid";
import type { PipelineReceipt } from "./types";

/**
 * Simple SHA-256 hash using Web Crypto API (browser) or Node.js crypto.
 * Used for receipt chain integrity — input/output payload hashing.
 */
async function sha256(data: string): Promise<string> {
  if (typeof window !== "undefined" && window.crypto?.subtle) {
    const encoded = new TextEncoder().encode(data);
    const hashBuffer = await window.crypto.subtle.digest("SHA-256", encoded);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  }
  // Node.js fallback
  const { createHash } = await import("crypto");
  return createHash("sha256").update(data).digest("hex");
}

// Stage names in pipeline order — spec §4 Stage 1-8
const STAGE_ORDER = [
  "STUDIO_CANVAS_INIT",
  "STUDIO_TIMELINE_INIT",
  "BPM_SYNC_APPLY",
  "LIP_SYNC_GENERATE",
  "BONE_OVERRIDE",
  "CHARACTER_FRAME_EXPORT",
  "SCENE_COMPOSITION",
  "CLIP_LIBRARY_IMPORT",
] as const;

const STAGE_AGENTS: Record<string, string> = {
  STUDIO_CANVAS_INIT: "animation_studio",
  STUDIO_TIMELINE_INIT: "animation_studio",
  BPM_SYNC_APPLY: "animation_studio",
  LIP_SYNC_GENERATE: "lip_sync_engine",
  BONE_OVERRIDE: "animation_studio",
  CHARACTER_FRAME_EXPORT: "animation_render_service",
  SCENE_COMPOSITION: "animation_studio",
  CLIP_LIBRARY_IMPORT: "library_importer",
};

/**
 * In-memory receipt chain. In production, this persists to the project's
 * receipt directory alongside the manifest.
 */
class ReceiptChain {
  private receipts: PipelineReceipt[] = [];

  /**
   * Emit a receipt for a pipeline stage.
   * Links to the previous receipt via hash chain.
   */
  async emit(
    stageName: string,
    inputPayload: unknown,
    outputPayload: unknown
  ): Promise<PipelineReceipt> {
    const agentName = STAGE_AGENTS[stageName];
    if (!agentName) {
      throw new Error(`Unknown stage name: ${stageName}. Valid stages: ${STAGE_ORDER.join(", ")}`);
    }

    const inputHash = await sha256(JSON.stringify(inputPayload));
    const outputHash = await sha256(JSON.stringify(outputPayload));

    const previousReceipt =
      this.receipts.length > 0 ? this.receipts[this.receipts.length - 1] : null;
    const previousHash = previousReceipt
      ? await sha256(JSON.stringify(previousReceipt))
      : "GENESIS";

    const receipt: PipelineReceipt = {
      receipt_id: uuidv4(),
      previous_receipt_hash: previousHash,
      input_payload_hash: inputHash,
      output_payload_hash: outputHash,
      stage_name: stageName,
      agent_name: agentName,
      timestamp: new Date().toISOString(),
    };

    this.receipts.push(receipt);
    return receipt;
  }

  /**
   * Get all receipts in chain order.
   */
  getAll(): PipelineReceipt[] {
    return [...this.receipts];
  }

  /**
   * Verify the chain is unbroken: each receipt's previous_receipt_hash
   * matches the SHA-256 of the prior receipt.
   */
  async verify(): Promise<{
    valid: boolean;
    broken_at?: number;
    message: string;
  }> {
    if (this.receipts.length === 0) {
      return { valid: true, message: "Empty chain — nothing to verify." };
    }

    // First receipt must have GENESIS as previous
    if (this.receipts[0].previous_receipt_hash !== "GENESIS") {
      return {
        valid: false,
        broken_at: 0,
        message: `Receipt 0 (${this.receipts[0].stage_name}) previous_receipt_hash is '${this.receipts[0].previous_receipt_hash}', expected 'GENESIS'.`,
      };
    }

    for (let i = 1; i < this.receipts.length; i++) {
      const expectedHash = await sha256(JSON.stringify(this.receipts[i - 1]));
      if (this.receipts[i].previous_receipt_hash !== expectedHash) {
        return {
          valid: false,
          broken_at: i,
          message: `Chain broken at receipt ${i} (${this.receipts[i].stage_name}). Expected previous_receipt_hash '${expectedHash.slice(0, 16)}...', got '${this.receipts[i].previous_receipt_hash.slice(0, 16)}...'.`,
        };
      }
    }

    return {
      valid: true,
      message: `Receipt chain verified: ${this.receipts.length} receipts, all linked correctly.`,
    };
  }

  /**
   * Export the chain as JSON for persistence.
   */
  toJSON(): string {
    return JSON.stringify(this.receipts, null, 2);
  }

  /**
   * Load a previously persisted chain.
   */
  fromJSON(json: string): void {
    this.receipts = JSON.parse(json);
  }

  /**
   * Get the final receipt ID (for Build Receipt reporting).
   */
  getFinalReceiptId(): string | null {
    return this.receipts.length > 0
      ? this.receipts[this.receipts.length - 1].receipt_id
      : null;
  }

  /**
   * Get stage count.
   */
  get length(): number {
    return this.receipts.length;
  }
}

// Singleton instance for the current studio session
export const receiptChain = new ReceiptChain();
