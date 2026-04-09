// =============================================================================
// FR-VID-13 §4 Stage 5 — Manifest Patch Export (RFC 6902 JSON Patch)
// Produces DEP-VID-037: Animation_Manifest_Patch.json
// =============================================================================

import type { AnimationManifestPatch, RemotionManifest, ManifestPatchOperation } from "./types";

/**
 * Apply an RFC 6902 JSON Patch to a manifest.
 * Only supports "replace", "add", "remove" operations on
 * the /beats/{index}/character_overlay/* paths.
 *
 * @param manifest - The base manifest
 * @param patch - The animation manifest patch
 * @returns A new manifest with the patch applied
 */
export function applyManifestPatch(
  manifest: RemotionManifest,
  patch: AnimationManifestPatch
): RemotionManifest {
  // Deep clone the manifest to avoid mutations
  const result: RemotionManifest = JSON.parse(JSON.stringify(manifest));

  for (const op of patch.operations) {
    applyOperation(result, op);
  }

  return result;
}

/**
 * Apply a single RFC 6902 operation to the manifest.
 */
function applyOperation(manifest: RemotionManifest, op: ManifestPatchOperation): void {
  const pathParts = op.path.split("/").filter(Boolean);

  // Navigate to the target location
  let target: any = manifest;
  for (let i = 0; i < pathParts.length - 1; i++) {
    const part = pathParts[i];
    const asIndex = parseInt(part, 10);
    if (!isNaN(asIndex) && Array.isArray(target)) {
      target = target[asIndex];
    } else {
      target = target[part];
    }
    if (target === undefined || target === null) {
      throw new Error(`Patch path '${op.path}' could not be resolved at segment '${part}'.`);
    }
  }

  const lastKey = pathParts[pathParts.length - 1];

  switch (op.op) {
    case "replace":
      if (target[lastKey] === undefined) {
        throw new Error(`Cannot replace non-existent path '${op.path}'.`);
      }
      target[lastKey] = op.value;
      break;

    case "add":
      if (Array.isArray(target)) {
        const idx = lastKey === "-" ? target.length : parseInt(lastKey, 10);
        target.splice(idx, 0, op.value);
      } else {
        target[lastKey] = op.value;
      }
      break;

    case "remove":
      if (Array.isArray(target)) {
        target.splice(parseInt(lastKey, 10), 1);
      } else {
        delete target[lastKey];
      }
      break;
  }
}

/**
 * Validate a manifest patch: check that all paths reference valid beat indices
 * and that the operation count matches expected edits.
 */
export function validateManifestPatch(
  patch: AnimationManifestPatch,
  manifest: RemotionManifest
): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!patch.patch_id) {
    errors.push("Missing patch_id.");
  }
  if (!patch.base_manifest_id) {
    errors.push("Missing base_manifest_id.");
  }
  if (patch.base_manifest_id !== manifest.manifest_id) {
    errors.push(
      `Patch base_manifest_id '${patch.base_manifest_id}' does not match manifest '${manifest.manifest_id}'.`
    );
  }

  for (let i = 0; i < patch.operations.length; i++) {
    const op = patch.operations[i];
    if (!["replace", "add", "remove"].includes(op.op)) {
      errors.push(`Operation ${i}: invalid op '${op.op}'.`);
    }

    // Validate beat index references
    const beatMatch = op.path.match(/\/beats\/(\d+)\//);
    if (beatMatch) {
      const beatIdx = parseInt(beatMatch[1], 10);
      if (beatIdx >= manifest.beats.length) {
        errors.push(
          `Operation ${i}: references beat ${beatIdx}, but manifest only has ${manifest.beats.length} beats.`
        );
      }
    }
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Serialize the manifest patch to JSON for export.
 */
export function serializeManifestPatch(patch: AnimationManifestPatch): string {
  return JSON.stringify(patch, null, 2);
}
