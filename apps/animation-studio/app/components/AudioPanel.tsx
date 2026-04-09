"use client";

// =============================================================================
// FR-VID-13 §4 Stage 2 Step 3 + §8 Task 8 — Audio Panel
// Features: waveform display (wavesurfer.js placeholder), volume controls,
//           BPM display, lip sync per-beat toggle
// =============================================================================

import React from "react";
import { useStudioStore } from "../store";

export function AudioPanel() {
  const voiceoverVolume = useStudioStore((s) => s.voiceoverVolume);
  const musicVolume = useStudioStore((s) => s.musicVolume);
  const setVoiceoverVolume = useStudioStore((s) => s.setVoiceoverVolume);
  const setMusicVolume = useStudioStore((s) => s.setMusicVolume);
  const bpmData = useStudioStore((s) => s.bpmData);
  const manifest = useStudioStore((s) => s.manifest);
  const selectedBeatIndex = useStudioStore((s) => s.selectedBeatIndex);
  const toggleLipSync = useStudioStore((s) => s.toggleLipSync);

  const selectedBeat = manifest?.beats[selectedBeatIndex];
  const lipSyncEnabled = selectedBeat?.character_overlay?.lip_sync_enabled ?? false;

  return (
    <div className="flex flex-col h-full">
      <div className="p-2 text-xs font-bold text-gray-400 border-b border-border uppercase">
        Audio Panel
      </div>

      <div className="flex-1 p-2 space-y-3">
        {/* Waveform placeholder — wavesurfer.js mounts here at runtime */}
        <div className="h-16 bg-[#1a1a1a] rounded border border-border flex items-center justify-center">
          <div id="waveform-container" className="w-full h-full" />
          <span className="text-[10px] text-gray-600 absolute">
            Waveform (wavesurfer.js)
          </span>
        </div>

        {/* BPM Display */}
        {bpmData && (
          <div className="flex items-center gap-2 text-xs">
            <span className="text-gray-400">BPM:</span>
            <span className="text-white font-bold">{bpmData.tempo_bpm}</span>
            <span className="text-gray-500">
              (confidence: {Math.round(bpmData.confidence * 100)}%)
            </span>
          </div>
        )}

        {/* Volume Controls */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <label className="text-[10px] text-gray-400 w-16">Voiceover</label>
            <input
              type="range"
              min={0}
              max={100}
              value={Math.round(voiceoverVolume * 100)}
              onChange={(e) => setVoiceoverVolume(parseInt(e.target.value, 10) / 100)}
              className="flex-1 h-1 accent-accent"
            />
            <span className="text-[10px] text-gray-500 w-8 text-right">
              {Math.round(voiceoverVolume * 100)}%
            </span>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-[10px] text-gray-400 w-16">Music</label>
            <input
              type="range"
              min={0}
              max={100}
              value={Math.round(musicVolume * 100)}
              onChange={(e) => setMusicVolume(parseInt(e.target.value, 10) / 100)}
              className="flex-1 h-1 accent-accent"
            />
            <span className="text-[10px] text-gray-500 w-8 text-right">
              {Math.round(musicVolume * 100)}%
            </span>
          </div>
        </div>

        {/* Per-Beat Lip Sync Toggle */}
        {manifest && (
          <div className="flex items-center gap-2 pt-1 border-t border-border">
            <button
              onClick={() => toggleLipSync(selectedBeatIndex)}
              className={`text-[10px] px-2 py-1 rounded transition-colors ${
                lipSyncEnabled
                  ? "bg-green-700 text-white"
                  : "bg-[#333] text-gray-400"
              }`}
            >
              🗣️ Lip Sync: {lipSyncEnabled ? "ON" : "OFF"}
            </button>
            <span className="text-[10px] text-gray-500">Beat {selectedBeatIndex}</span>
          </div>
        )}
      </div>
    </div>
  );
}
