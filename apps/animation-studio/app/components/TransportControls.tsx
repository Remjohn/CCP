"use client";

// =============================================================================
// FR-VID-13 §8 Task 18 — Transport Controls
// Features: play, pause, stop, frame step, loop beat, loop all,
//           playback speed (0.25x-2x), frame counter
// =============================================================================

import React from "react";
import { useStudioStore } from "../store";
import type { PlaybackSpeed, TargetFormat } from "../types";

const PLAYBACK_SPEEDS: PlaybackSpeed[] = [0.25, 0.5, 1, 1.5, 2];
const FORMATS: TargetFormat[] = ["9:16", "1:1", "16:9", "4:5"];

export function TransportControls() {
  const isPlaying = useStudioStore((s) => s.isPlaying);
  const currentFrame = useStudioStore((s) => s.currentFrame);
  const loopBeat = useStudioStore((s) => s.loopBeat);
  const loopAll = useStudioStore((s) => s.loopAll);
  const playbackSpeed = useStudioStore((s) => s.playbackSpeed);
  const play = useStudioStore((s) => s.play);
  const pause = useStudioStore((s) => s.pause);
  const stop = useStudioStore((s) => s.stop);
  const stepForward = useStudioStore((s) => s.stepForward);
  const stepBackward = useStudioStore((s) => s.stepBackward);
  const toggleLoopBeat = useStudioStore((s) => s.toggleLoopBeat);
  const toggleLoopAll = useStudioStore((s) => s.toggleLoopAll);
  const setPlaybackSpeed = useStudioStore((s) => s.setPlaybackSpeed);
  const targetFormat = useStudioStore((s) => s.targetFormat);
  const setTargetFormat = useStudioStore((s) => s.setTargetFormat);
  const manifest = useStudioStore((s) => s.manifest);
  const selectedBeatIndex = useStudioStore((s) => s.selectedBeatIndex);

  const selectedBeat = manifest?.beats[selectedBeatIndex];
  const beatDuration = selectedBeat?.duration_frames ?? 0;

  return (
    <div className="flex items-center gap-3 px-4 py-2 bg-panel border-t border-border">
      {/* Transport Buttons */}
      <div className="flex items-center gap-1">
        <button
          onClick={stepBackward}
          className="w-7 h-7 flex items-center justify-center rounded bg-[#333] hover:bg-[#444] text-white text-xs"
          title="Step Back (1 frame)"
        >
          ◁
        </button>
        <button
          onClick={stop}
          className="w-7 h-7 flex items-center justify-center rounded bg-[#333] hover:bg-[#444] text-white text-xs"
          title="Stop"
        >
          ■
        </button>
        <button
          onClick={isPlaying ? pause : play}
          className={`w-8 h-8 flex items-center justify-center rounded text-white text-sm ${
            isPlaying ? "bg-yellow-600 hover:bg-yellow-700" : "bg-green-600 hover:bg-green-700"
          }`}
          title={isPlaying ? "Pause" : "Play"}
        >
          {isPlaying ? "⏸" : "▶"}
        </button>
        <button
          onClick={stepForward}
          className="w-7 h-7 flex items-center justify-center rounded bg-[#333] hover:bg-[#444] text-white text-xs"
          title="Step Forward (1 frame)"
        >
          ▷
        </button>
      </div>

      {/* Frame Counter */}
      <div className="text-xs font-mono text-gray-300 min-w-[100px]">
        F: {String(currentFrame).padStart(4, "0")}
        {beatDuration > 0 && (
          <span className="text-gray-500"> / {String(beatDuration).padStart(4, "0")}</span>
        )}
      </div>

      {/* Loop Controls */}
      <div className="flex items-center gap-1">
        <button
          onClick={toggleLoopBeat}
          className={`text-[10px] px-2 py-1 rounded transition-colors ${
            loopBeat ? "bg-accent text-white" : "bg-[#333] text-gray-400"
          }`}
          title="Loop current beat"
        >
          🔁 Beat
        </button>
        <button
          onClick={toggleLoopAll}
          className={`text-[10px] px-2 py-1 rounded transition-colors ${
            loopAll ? "bg-accent text-white" : "bg-[#333] text-gray-400"
          }`}
          title="Loop all beats"
        >
          🔁 All
        </button>
      </div>

      {/* Playback Speed */}
      <div className="flex items-center gap-1">
        <span className="text-[10px] text-gray-400">Speed:</span>
        <select
          value={playbackSpeed}
          onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value) as PlaybackSpeed)}
          className="bg-[#333] border border-border rounded text-xs text-white px-1 py-0.5"
        >
          {PLAYBACK_SPEEDS.map((s) => (
            <option key={s} value={s}>
              {s}×
            </option>
          ))}
        </select>
      </div>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Format Selector */}
      <div className="flex items-center gap-1">
        <span className="text-[10px] text-gray-400">Format:</span>
        {FORMATS.map((f) => (
          <button
            key={f}
            onClick={() => setTargetFormat(f)}
            className={`text-[10px] px-2 py-1 rounded transition-colors ${
              targetFormat === f ? "bg-accent text-white" : "bg-[#333] text-gray-400"
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Beat Info */}
      <div className="text-[10px] text-gray-500">
        Beat {selectedBeatIndex}
        {selectedBeat && ` · ${selectedBeat.arc_stage}`}
      </div>
    </div>
  );
}
