"use client";

// =============================================================================
// FR-VID-13 — CCP Animation Studio Main Page
// 6-Panel Editor: Canvas, Clip Library, Beat Timeline, Bone Inspector,
//                 Layer Manager, Audio Panel + Transport Controls
// Gate O enforcement on load.
// =============================================================================

import React, { useEffect, useState } from "react";
import { useStudioStore } from "./store";
import { runGateO } from "./gate-o";
import { receiptChain } from "./receipt-chain";
import { serializeManifestPatch } from "./manifest-patch";
import {
  ClipLibrary,
  BeatTimeline,
  BoneInspector,
  LayerManager,
  AudioPanel,
  TransportControls,
} from "./components";
import type { TargetFormat } from "./types";

export default function StudioEditorPage() {
  const [gateStatus, setGateStatus] = useState<"LOADING" | "PASS" | "FAIL" | "LEGACY">("LOADING");
  const [gateErrors, setGateErrors] = useState<string[]>([]);
  const [gateWarnings, setGateWarnings] = useState<string[]>([]);
  const store = useStudioStore();

  // Gate O evaluation on boot
  useEffect(() => {
    const evaluateGate = async () => {
      try {
        // Determine audio URLs from first beat (if available)
        const firstBeat = store.manifest?.beats[0];
        const voiceoverUrl = firstBeat?.voiceover_url ?? null;
        const musicUrl = firstBeat?.music_url ?? null;

        const result = await runGateO(
          store.characterPackage,
          store.manifest,
          store.clipLibrary,
          store.forceAuthMode,
          store.targetFormat,
          voiceoverUrl,
          musicUrl
        );

        if (result.passed) {
          setGateStatus("PASS");
          // Emit receipt for STUDIO_CANVAS_INIT
          await receiptChain.emit(
            "STUDIO_CANVAS_INIT",
            { character: store.characterPackage?.character_id, format: store.targetFormat },
            { gate_o_result: "PASS", details: result.details.length }
          );
        } else {
          // Check for §7 backward compatibility fallback
          const q2Failure = result.details.find(
            (d) => d.question.includes("Q2") && !d.passed
          );
          if (q2Failure && !store.forceAuthMode) {
            // Apply §7 fallback: character authoring mode
            setGateStatus("LEGACY");
            setGateWarnings([
              "LEGACY_MANIFEST_NO_CHARACTER: Manifest does not contain character_overlay fields.",
              "Opening in character authoring mode. All beats default to idle_breathe + SC-01.",
              "Consider re-running the AnimationDirectorAgent for auto-selection.",
            ]);
          } else {
            setGateStatus("FAIL");
            setGateErrors(result.errors);
          }
        }
      } catch (err: any) {
        setGateStatus("FAIL");
        setGateErrors([err.message || "Unknown error during Gate O evaluation"]);
      }
    };

    evaluateGate();
  }, [store.characterPackage, store.manifest, store.clipLibrary, store.forceAuthMode, store.targetFormat]);

  // Export manifest patch handler
  const handleExportPatch = async () => {
    const patch = store.generateManifestPatch();
    const json = serializeManifestPatch(patch);

    // Emit receipt for BONE_OVERRIDE stage
    await receiptChain.emit(
      "BONE_OVERRIDE",
      { beat_count: store.manifest?.beats.length, operations: patch.operations.length },
      { patch_id: patch.patch_id, operation_count: patch.operations.length }
    );

    // Download as file
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${patch.patch_id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // --- LOADING ---
  if (gateStatus === "LOADING") {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-[#1a1a1a] text-white">
        <div className="flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin" />
          <span className="text-sm text-gray-400">Evaluating Gate O constraints...</span>
        </div>
      </div>
    );
  }

  // --- GATE FAIL ---
  if (gateStatus === "FAIL") {
    return (
      <div className="h-screen w-screen flex flex-col items-center justify-center bg-[#1a1a1a] text-red-400 p-8">
        <h1 className="text-2xl font-bold mb-2">Gate O — Pre-Session Constraint Failed</h1>
        <p className="text-sm text-gray-400 mb-6">The Animation Studio cannot open until all constraints are satisfied.</p>
        <ul className="space-y-2 max-w-2xl">
          {gateErrors.map((err, i) => (
            <li key={i} className="flex items-start gap-2 text-sm">
              <span className="text-red-500 mt-0.5">✗</span>
              <span>{err}</span>
            </li>
          ))}
        </ul>
      </div>
    );
  }

  // --- MAIN EDITOR (PASS or LEGACY mode) ---
  return (
    <div className="h-screen w-screen flex flex-col bg-[#1a1a1a] text-white overflow-hidden">
      {/* Legacy Warning Banner (§7) */}
      {gateStatus === "LEGACY" && (
        <div className="bg-yellow-900/50 border-b border-yellow-700 px-4 py-2">
          <div className="flex items-center gap-2 text-xs text-yellow-300">
            <span>⚠️</span>
            <span>LEGACY_MANIFEST_NO_CHARACTER — Character Authoring Mode. {gateWarnings[2]}</span>
          </div>
        </div>
      )}

      {/* Top Header Bar */}
      <div className="h-12 border-b border-[#333] bg-[#242424] flex items-center px-4 justify-between flex-shrink-0">
        <div className="flex items-center gap-3">
          <span className="font-semibold tracking-wide text-sm">CCP Animation Studio</span>
          {store.characterPackage && (
            <span className="text-xs text-gray-400">
              {store.characterPackage.display_name}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {/* Patch operation count */}
          {store.patchOperations.length > 0 && (
            <span className="text-[10px] text-yellow-400 px-2 py-0.5 bg-yellow-900/30 rounded">
              {store.patchOperations.length} changes
            </span>
          )}
          {/* Review Notes */}
          <input
            type="text"
            placeholder="Review notes..."
            value={store.reviewNotes}
            onChange={(e) => store.setReviewNotes(e.target.value)}
            className="bg-[#1a1a1a] border border-[#333] rounded px-2 py-1 text-xs text-white placeholder-gray-500 w-48"
          />
          {/* Export Patch Button */}
          <button
            onClick={handleExportPatch}
            disabled={store.patchOperations.length === 0}
            className="text-xs px-3 py-1.5 bg-green-700 hover:bg-green-600 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded transition-colors"
          >
            Export Patch ({store.patchOperations.length})
          </button>
        </div>
      </div>

      {/* Main 3-Column Layout */}
      <div className="flex-1 flex flex-row overflow-hidden">
        {/* Left Sidebar — Clip Library */}
        <div className="w-64 border-r border-[#333] bg-[#242424] flex flex-col flex-shrink-0">
          <ClipLibrary />
        </div>

        {/* Center — Canvas + Timeline */}
        <div className="flex-1 flex flex-col h-full bg-[#111]">
          {/* Canvas Area (PixiJS + DragonBonesJS renders here) */}
          <div className="flex-1 relative flex items-center justify-center overflow-hidden bg-[#0a0a0a]">
            <div
              id="pixi-canvas-container"
              className="relative"
              style={{
                width: 512,
                height: 768,
                border: "1px solid #333",
                backgroundColor: "transparent",
              }}
            >
              {/* PixiJS Application mounts here via useEffect */}
              <div className="absolute inset-0 flex items-center justify-center text-gray-600 text-xs">
                {store.characterPackage
                  ? `${store.characterPackage.character_id} — ${store.targetFormat}`
                  : "Load a character package to begin"}
              </div>
            </div>
          </div>

          {/* Timeline + Audio — Bottom Half */}
          <div className="h-56 border-t border-[#333] bg-[#242424] flex flex-row flex-shrink-0">
            <div className="flex-1 border-r border-[#333]">
              <BeatTimeline />
            </div>
            <div className="w-72">
              <AudioPanel />
            </div>
          </div>
        </div>

        {/* Right Sidebar — Layer Manager + Bone Inspector */}
        <div className="w-72 border-l border-[#333] bg-[#242424] flex flex-col flex-shrink-0">
          <div className="h-1/3 border-b border-[#333]">
            <LayerManager />
          </div>
          <div className="flex-1">
            <BoneInspector />
          </div>
        </div>
      </div>

      {/* Transport Controls Bar */}
      <TransportControls />
    </div>
  );
}
