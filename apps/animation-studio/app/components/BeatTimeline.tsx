"use client";

// =============================================================================
// FR-VID-13 §4 Stage 2 — Beat Timeline Panel
// Features: beat blocks, playhead, drag-to-swap, transition markers, BPM grid
// =============================================================================

import React, { useRef, useCallback } from "react";
import { useStudioStore } from "../store";
import type { SceneId } from "../types";

const BEAT_BLOCK_WIDTH = 120;
const TIMELINE_HEIGHT = 80;

const ARC_COLORS: Record<string, string> = {
  hook: "#e74c3c",
  tension: "#e67e22",
  relief: "#f1c40f",
  dopamine: "#2ecc71",
  revelation: "#3498db",
  transformation: "#9b59b6",
  resolution: "#1abc9c",
  default: "#555",
};

const TRANSITION_ICONS: Record<string, string> = {
  crossfade: "⤳",
  cut: "✂",
  push: "→",
};

export function BeatTimeline() {
  const manifest = useStudioStore((s) => s.manifest);
  const selectedBeatIndex = useStudioStore((s) => s.selectedBeatIndex);
  const selectBeat = useStudioStore((s) => s.selectBeat);
  const swapClipOnBeat = useStudioStore((s) => s.swapClipOnBeat);
  const currentFrame = useStudioStore((s) => s.currentFrame);
  const bpmData = useStudioStore((s) => s.bpmData);
  const timelineRef = useRef<HTMLDivElement>(null);

  const handleBeatClick = useCallback(
    (idx: number) => {
      selectBeat(idx);
    },
    [selectBeat]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent, beatIndex: number) => {
      e.preventDefault();
      const clipId = e.dataTransfer.getData("application/x-clip-id");
      if (clipId) {
        swapClipOnBeat(beatIndex, clipId);
      }
    },
    [swapClipOnBeat]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "copy";
  }, []);

  if (!manifest) {
    return (
      <div className="h-full flex items-center justify-center text-sm text-gray-500">
        No manifest loaded
      </div>
    );
  }

  const totalFrames = manifest.beats.reduce((sum, b) => sum + b.duration_frames, 0);

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-2 py-1 border-b border-border">
        <span className="text-xs font-bold text-gray-400 uppercase">Beat Timeline</span>
        <span className="text-[10px] text-gray-500">
          {manifest.beats.length} beats · {totalFrames} frames · {manifest.fps} FPS
          {bpmData && ` · ${bpmData.tempo_bpm} BPM`}
        </span>
      </div>

      {/* Timeline Scroll Area */}
      <div
        ref={timelineRef}
        className="flex-1 overflow-x-auto overflow-y-hidden"
        style={{ minHeight: TIMELINE_HEIGHT }}
      >
        <div
          className="relative flex items-stretch"
          style={{
            width: manifest.beats.length * BEAT_BLOCK_WIDTH,
            height: TIMELINE_HEIGHT,
          }}
        >
          {/* BPM Grid Lines */}
          {bpmData &&
            bpmData.beat_times_sec.map((time, i) => {
              const framePos = Math.round(time * manifest.fps);
              const pxPos = (framePos / totalFrames) * (manifest.beats.length * BEAT_BLOCK_WIDTH);
              return (
                <div
                  key={`bpm-${i}`}
                  className="absolute top-0 bottom-0 w-px"
                  style={{
                    left: pxPos,
                    backgroundColor: i % 4 === 0 ? "rgba(46,204,113,0.5)" : "rgba(128,128,128,0.25)",
                    zIndex: 1,
                  }}
                />
              );
            })}

          {/* Beat Blocks */}
          {manifest.beats.map((beat, idx) => {
            const color = ARC_COLORS[beat.arc_stage] || ARC_COLORS.default;
            const isSelected = idx === selectedBeatIndex;

            return (
              <React.Fragment key={beat.beat_index}>
                <div
                  onClick={() => handleBeatClick(idx)}
                  onDrop={(e) => handleDrop(e, idx)}
                  onDragOver={handleDragOver}
                  className={`relative flex flex-col justify-between p-1.5 cursor-pointer border-r transition-all ${
                    isSelected
                      ? "ring-2 ring-accent ring-inset"
                      : "hover:brightness-125"
                  }`}
                  style={{
                    width: BEAT_BLOCK_WIDTH,
                    backgroundColor: `${color}22`,
                    borderColor: "#333",
                  }}
                >
                  {/* Top: beat index + type */}
                  <div className="flex justify-between items-start">
                    <span
                      className="text-[10px] font-bold px-1 rounded"
                      style={{ backgroundColor: color, color: "#fff" }}
                    >
                      {beat.beat_index}
                    </span>
                    <span className="text-[9px] text-gray-400">{beat.beat_type}</span>
                  </div>

                  {/* Center: clip name */}
                  <div className="text-[10px] text-gray-300 truncate text-center">
                    {beat.character_overlay?.animation_primary || "—"}
                  </div>

                  {/* Bottom: scene + lip sync indicator */}
                  <div className="flex justify-between items-end">
                    <span className="text-[9px] text-gray-500">
                      {beat.character_overlay?.scene_id || "—"}
                    </span>
                    {beat.character_overlay?.lip_sync_enabled && (
                      <span className="text-[10px]" title="Lip Sync ON">🗣️</span>
                    )}
                  </div>
                </div>

                {/* Transition marker */}
                {idx < manifest.beats.length - 1 && beat.transition_type && (
                  <div
                    className="absolute top-1/2 -translate-y-1/2 text-xs text-gray-500 z-10"
                    style={{ left: (idx + 1) * BEAT_BLOCK_WIDTH - 8 }}
                    title={beat.transition_type}
                  >
                    {TRANSITION_ICONS[beat.transition_type] || "·"}
                  </div>
                )}
              </React.Fragment>
            );
          })}

          {/* Playhead */}
          <div
            className="absolute top-0 bottom-0 w-0.5 bg-red-500 z-20 pointer-events-none"
            style={{
              left: (currentFrame / totalFrames) * (manifest.beats.length * BEAT_BLOCK_WIDTH),
            }}
          />
        </div>
      </div>
    </div>
  );
}
