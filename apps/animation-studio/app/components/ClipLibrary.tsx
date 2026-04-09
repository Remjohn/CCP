"use client";

// =============================================================================
// FR-VID-13 §4 Stage 2 — Clip Library Panel
// Categories: Emotions (17), Gestures (8), Loops (5), Interactions (6), Scenes (8)
// Features: search/filter, thumbnail, drag-to-timeline
// =============================================================================

import React, { useMemo } from "react";
import { useStudioStore } from "../store";
import type { AnimationClip } from "../types";

const CATEGORIES = ["Emotions", "Gestures", "Loops", "Interactions", "Scenes"] as const;

export function ClipLibrary() {
  const clipLibrary = useStudioStore((s) => s.clipLibrary);
  const clipSearchQuery = useStudioStore((s) => s.clipSearchQuery);
  const setClipSearchQuery = useStudioStore((s) => s.setClipSearchQuery);
  const clipCategoryFilter = useStudioStore((s) => s.clipCategoryFilter);
  const setClipCategoryFilter = useStudioStore((s) => s.setClipCategoryFilter);
  const selectedBeatIndex = useStudioStore((s) => s.selectedBeatIndex);
  const swapClipOnBeat = useStudioStore((s) => s.swapClipOnBeat);

  const filteredClips = useMemo(() => {
    if (!clipLibrary) return [];
    let clips = clipLibrary.clips;

    if (clipCategoryFilter) {
      clips = clips.filter((c) => c.category === clipCategoryFilter);
    }

    if (clipSearchQuery.trim()) {
      const q = clipSearchQuery.toLowerCase();
      clips = clips.filter(
        (c) =>
          c.name.toLowerCase().includes(q) ||
          c.clip_id.toLowerCase().includes(q) ||
          c.affected_bones.some((b) => b.toLowerCase().includes(q))
      );
    }

    return clips;
  }, [clipLibrary, clipSearchQuery, clipCategoryFilter]);

  function handleDragStart(e: React.DragEvent, clip: AnimationClip) {
    e.dataTransfer.setData("application/x-clip-id", clip.clip_id);
    e.dataTransfer.effectAllowed = "copy";
  }

  function handleClipClick(clip: AnimationClip) {
    // Preview on canvas - swap on selected beat
    swapClipOnBeat(selectedBeatIndex, clip.clip_id);
  }

  if (!clipLibrary) {
    return (
      <div className="flex flex-col h-full">
        <div className="p-2 text-xs font-bold text-gray-400 border-b border-border uppercase">
          Clip Library
        </div>
        <div className="flex-1 flex items-center justify-center text-sm text-gray-500">
          No library loaded
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <div className="p-2 text-xs font-bold text-gray-400 border-b border-border uppercase">
        Clip Library ({clipLibrary.clips.length})
      </div>

      {/* Search */}
      <div className="p-2 border-b border-border">
        <input
          type="text"
          placeholder="Search clips..."
          value={clipSearchQuery}
          onChange={(e) => setClipSearchQuery(e.target.value)}
          className="w-full bg-[#1a1a1a] border border-border rounded px-2 py-1 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-accent"
        />
      </div>

      {/* Category Tabs */}
      <div className="flex flex-wrap gap-1 p-2 border-b border-border">
        <button
          onClick={() => setClipCategoryFilter(null)}
          className={`text-[10px] px-2 py-0.5 rounded ${
            !clipCategoryFilter ? "bg-accent text-white" : "bg-[#333] text-gray-400"
          }`}
        >
          All
        </button>
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setClipCategoryFilter(cat)}
            className={`text-[10px] px-2 py-0.5 rounded ${
              clipCategoryFilter === cat ? "bg-accent text-white" : "bg-[#333] text-gray-400"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Clip List */}
      <div className="flex-1 overflow-y-auto">
        {filteredClips.map((clip) => (
          <div
            key={clip.clip_id}
            draggable
            onDragStart={(e) => handleDragStart(e, clip)}
            onClick={() => handleClipClick(clip)}
            className="p-2 border-b border-border cursor-pointer hover:bg-[#333] transition-colors"
            title={`Drag to timeline beat to swap animation.\nBones: ${clip.affected_bones.join(", ")}`}
          >
            <div className="flex items-center gap-2">
              {/* Thumbnail placeholder */}
              <div className="w-10 h-10 bg-[#2a2a2a] rounded flex items-center justify-center text-[8px] text-gray-500 flex-shrink-0">
                {clip.category.slice(0, 3).toUpperCase()}
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-xs font-medium text-white truncate">{clip.name}</div>
                <div className="text-[10px] text-gray-500">
                  {clip.duration_frames}f · {clip.affected_bones.length} bones
                  {clip.source === "imported" && ` · ${clip.original_format}`}
                </div>
              </div>
            </div>
          </div>
        ))}
        {filteredClips.length === 0 && (
          <div className="p-4 text-center text-xs text-gray-500">No clips match filter.</div>
        )}
      </div>
    </div>
  );
}
