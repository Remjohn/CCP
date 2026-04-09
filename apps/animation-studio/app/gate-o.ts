// =============================================================================
// FR-VID-13 §6 — Gate O: Pre-Session Constraint Network
// (Animation Studio Integrity Assurance)
// 6 questions, each an executable validation function returning boolean + diagnostic.
// Spec Reference: §6 Skill Definition, Gate M → renamed Gate O per build flag resolution.
// =============================================================================

import type {
  CharacterPackage,
  AnimationClipLibrary,
  RemotionManifest,
  TargetFormat,
} from "./types";

export interface GateQuestionResult {
  question: string;
  passed: boolean;
  diagnostic: string;
}

export interface GateResult {
  passed: boolean;
  errors: string[];
  details: GateQuestionResult[];
}

// ---------------------------------------------------------------------------
// Q1: Character Package Completeness
// "Does the character_package.json contain valid layers[] with resolvable PNG URLs
//  and a skeleton with at least 15 bones?"
// ---------------------------------------------------------------------------
export function validateCharacterPackage(
  pkg: CharacterPackage | null
): GateQuestionResult {
  const question = "Q1: Character Package Completeness";

  if (!pkg) {
    return { question, passed: false, diagnostic: "No character package loaded." };
  }

  if (!Array.isArray(pkg.layers) || pkg.layers.length === 0) {
    return {
      question,
      passed: false,
      diagnostic: `Character package '${pkg.character_id}' has ${pkg.layers?.length ?? 0} layers. At least 1 required.`,
    };
  }

  for (const layer of pkg.layers) {
    if (!layer.png_url || typeof layer.png_url !== "string") {
      return {
        question,
        passed: false,
        diagnostic: `Layer '${layer.name}' has invalid or missing png_url.`,
      };
    }
    if (!layer.bone || typeof layer.bone !== "string") {
      return {
        question,
        passed: false,
        diagnostic: `Layer '${layer.name}' has invalid or missing bone binding.`,
      };
    }
  }

  if (!pkg.skeleton) {
    return { question, passed: false, diagnostic: "Character package has no skeleton." };
  }

  if (!Array.isArray(pkg.skeleton.bones) || pkg.skeleton.bones.length < 15) {
    return {
      question,
      passed: false,
      diagnostic: `Skeleton has ${pkg.skeleton.bones?.length ?? 0} bones. Minimum 15 required.`,
    };
  }

  if (!pkg.skeleton.root_bone) {
    return { question, passed: false, diagnostic: "Skeleton has no root_bone defined." };
  }

  return {
    question,
    passed: true,
    diagnostic: `Character '${pkg.character_id}' loaded: ${pkg.layers.length} layers, ${pkg.skeleton.bones.length} bones.`,
  };
}

// ---------------------------------------------------------------------------
// Q2: Manifest Character Overlay
// "Does every beat in the manifest have a character_overlay field with
//  animation_primary and scene_id populated?"
// Exception: If force_auth_mode == true, bypass and allow §7 fallback.
// ---------------------------------------------------------------------------
export function validateManifestCharacterOverlay(
  manifest: RemotionManifest | null,
  forceAuthMode: boolean
): GateQuestionResult {
  const question = "Q2: Manifest Character Overlay";

  if (!manifest) {
    return { question, passed: false, diagnostic: "No manifest loaded." };
  }

  if (forceAuthMode) {
    return {
      question,
      passed: true,
      diagnostic: "force_auth_mode=true: bypassing overlay check. §7 fallback logic applies.",
    };
  }

  if (!Array.isArray(manifest.beats) || manifest.beats.length === 0) {
    return { question, passed: false, diagnostic: "Manifest has no beats." };
  }

  for (const beat of manifest.beats) {
    if (!beat.character_overlay) {
      return {
        question,
        passed: false,
        diagnostic: `Beat ${beat.beat_index} has no character_overlay field. Run AnimationDirectorAgent first.`,
      };
    }
    if (!beat.character_overlay.animation_primary) {
      return {
        question,
        passed: false,
        diagnostic: `Beat ${beat.beat_index} character_overlay.animation_primary is empty.`,
      };
    }
    if (!beat.character_overlay.scene_id) {
      return {
        question,
        passed: false,
        diagnostic: `Beat ${beat.beat_index} character_overlay.scene_id is empty.`,
      };
    }
  }

  return {
    question,
    passed: true,
    diagnostic: `All ${manifest.beats.length} beats have valid character_overlay with animation_primary and scene_id.`,
  };
}

// ---------------------------------------------------------------------------
// Q3: Clip Library Availability
// "Are all clip IDs referenced in the manifest present in the clip library?"
// ---------------------------------------------------------------------------
export function validateClipLibrary(
  manifest: RemotionManifest | null,
  library: AnimationClipLibrary | null,
  forceAuthMode: boolean
): GateQuestionResult {
  const question = "Q3: Clip Library Availability";

  if (!library) {
    return { question, passed: false, diagnostic: "No clip library loaded." };
  }

  if (!manifest || forceAuthMode) {
    // If force_auth_mode, we only need the library to exist, not validate against manifest
    return {
      question,
      passed: true,
      diagnostic: `Clip library loaded: ${library.clips.length} clips. ${forceAuthMode ? "(force_auth_mode — manifest clips not validated)" : "(no manifest to validate against)"}`,
    };
  }

  const libraryClipIds = new Set(library.clips.map((c) => c.clip_id));
  const missingClips: string[] = [];

  for (const beat of manifest.beats) {
    if (beat.character_overlay?.animation_primary) {
      if (!libraryClipIds.has(beat.character_overlay.animation_primary)) {
        missingClips.push(
          `Beat ${beat.beat_index}: '${beat.character_overlay.animation_primary}'`
        );
      }
    }
  }

  if (missingClips.length > 0) {
    return {
      question,
      passed: false,
      diagnostic: `Missing clips in library: ${missingClips.join(", ")}`,
    };
  }

  return {
    question,
    passed: true,
    diagnostic: `All manifest clip references found in library (${library.clips.length} clips available).`,
  };
}

// ---------------------------------------------------------------------------
// Q4: Audio Asset Presence
// "Are both voiceover and music audio files accessible?"
// ---------------------------------------------------------------------------
export async function validateAudioPresence(
  voiceoverUrl: string | null,
  musicUrl: string | null
): Promise<GateQuestionResult> {
  const question = "Q4: Audio Asset Presence";

  const errors: string[] = [];

  if (!voiceoverUrl) {
    errors.push("Voiceover URL is missing.");
  } else {
    try {
      const resp = await fetch(voiceoverUrl, { method: "HEAD" });
      if (!resp.ok) {
        errors.push(`Voiceover not accessible: HTTP ${resp.status}`);
      }
    } catch (err: any) {
      errors.push(`Voiceover fetch failed: ${err.message}`);
    }
  }

  if (!musicUrl) {
    errors.push("Music URL is missing.");
  } else {
    try {
      const resp = await fetch(musicUrl, { method: "HEAD" });
      if (!resp.ok) {
        errors.push(`Music not accessible: HTTP ${resp.status}`);
      }
    } catch (err: any) {
      errors.push(`Music fetch failed: ${err.message}`);
    }
  }

  if (errors.length > 0) {
    return { question, passed: false, diagnostic: errors.join("; ") };
  }

  return { question, passed: true, diagnostic: "Voiceover and music audio files are accessible." };
}

// ---------------------------------------------------------------------------
// Q5: Format Specification
// "Is the target output format specified (9:16, 1:1, 16:9, 4:5)?"
// Default to 9:16 if unspecified.
// ---------------------------------------------------------------------------
export function validateFormatSpecification(
  format: TargetFormat | string | null
): GateQuestionResult {
  const question = "Q5: Format Specification";
  const validFormats: TargetFormat[] = ["9:16", "1:1", "16:9", "4:5"];

  if (!format) {
    return {
      question,
      passed: true,
      diagnostic: "No format specified. Defaulting to 9:16.",
    };
  }

  if (!validFormats.includes(format as TargetFormat)) {
    return {
      question,
      passed: false,
      diagnostic: `Invalid format '${format}'. Must be one of: ${validFormats.join(", ")}`,
    };
  }

  return {
    question,
    passed: true,
    diagnostic: `Target format: ${format}`,
  };
}

// ---------------------------------------------------------------------------
// Q6: Export Pipeline Ready
// "Is the headless frame export service running and connected?"
// ---------------------------------------------------------------------------
export async function validateExportPipelineReady(
  exportServiceUrl?: string
): Promise<GateQuestionResult> {
  const question = "Q6: Export Pipeline Ready";
  const url = exportServiceUrl || "/api/export/health";

  try {
    const resp = await fetch(url, { method: "GET", signal: AbortSignal.timeout(5000) });
    if (resp.ok) {
      return { question, passed: true, diagnostic: `Export service is healthy at ${url}.` };
    }
    return {
      question,
      passed: false,
      diagnostic: `Export service returned HTTP ${resp.status}. Frame export will be unavailable.`,
    };
  } catch (err: any) {
    // Q6 failure is a WARNING, not a hard block (per spec: "display a clear warning")
    return {
      question,
      passed: true, // Soft pass — display warning in UI
      diagnostic: `⚠️ Export service unreachable at ${url}: ${err.message}. Export button will show warning.`,
    };
  }
}

// ---------------------------------------------------------------------------
// runGateO: Orchestrator — runs all 6 questions
// ---------------------------------------------------------------------------
export async function runGateO(
  characterPackage?: CharacterPackage | null,
  manifest?: RemotionManifest | null,
  clipLibrary?: AnimationClipLibrary | null,
  forceAuthMode?: boolean,
  targetFormat?: TargetFormat | null,
  voiceoverUrl?: string | null,
  musicUrl?: string | null,
  exportServiceUrl?: string
): Promise<GateResult> {
  const results: GateQuestionResult[] = [];

  // Q1
  results.push(validateCharacterPackage(characterPackage ?? null));

  // Q2
  results.push(
    validateManifestCharacterOverlay(manifest ?? null, forceAuthMode ?? false)
  );

  // Q3
  results.push(
    validateClipLibrary(manifest ?? null, clipLibrary ?? null, forceAuthMode ?? false)
  );

  // Q4 (async)
  results.push(
    await validateAudioPresence(voiceoverUrl ?? null, musicUrl ?? null)
  );

  // Q5
  results.push(validateFormatSpecification(targetFormat ?? null));

  // Q6 (async)
  results.push(await validateExportPipelineReady(exportServiceUrl));

  const errors = results.filter((r) => !r.passed).map((r) => `${r.question}: ${r.diagnostic}`);

  return {
    passed: errors.length === 0,
    errors,
    details: results,
  };
}
