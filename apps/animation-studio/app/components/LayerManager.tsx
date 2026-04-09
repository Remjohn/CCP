"use client";

// =============================================================================
// FR-VID-13 §8 Task 7 — Layer Manager Panel
// Features: visibility toggles, z-order drag/reorder, opacity slider per layer
// =============================================================================

import React from "react";
import { useStudioStore } from "../store";

export function LayerManager() {
  const characterPackage = useStudioStore((s) => s.characterPackage);
  const layerVisibility = useStudioStore((s) => s.layerVisibility);
  const toggleLayerVisibility = useStudioStore((s) => s.toggleLayerVisibility);
  const layerOpacity = useStudioStore((s) => s.layerOpacity);
  const setLayerOpacity = useStudioStore((s) => s.setLayerOpacity);
  const layerOrder = useStudioStore((s) => s.layerOrder);
  const reorderLayers = useStudioStore((s) => s.reorderLayers);

  const [dragIndex, setDragIndex] = React.useState<number | null>(null);

  function handleDragStart(e: React.DragEvent, index: number) {
    setDragIndex(index);
    e.dataTransfer.effectAllowed = "move";
  }

  function handleDragOver(e: React.DragEvent) {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
  }

  function handleDrop(e: React.DragEvent, targetIndex: number) {
    e.preventDefault();
    if (dragIndex !== null && dragIndex !== targetIndex) {
      reorderLayers(dragIndex, targetIndex);
    }
    setDragIndex(null);
  }

  if (!characterPackage) {
    return (
      <div className="flex flex-col h-full">
        <div className="p-2 text-xs font-bold text-gray-400 border-b border-border uppercase">
          Layer Manager
        </div>
        <div className="flex-1 flex items-center justify-center text-sm text-gray-500">
          No character loaded
        </div>
      </div>
    );
  }

  // Resolve layers from order
  const layers = layerOrder
    .map((name) => characterPackage.layers.find((l) => l.name === name))
    .filter(Boolean);

  return (
    <div className="flex flex-col h-full">
      <div className="p-2 text-xs font-bold text-gray-400 border-b border-border uppercase">
        Layer Manager ({layers.length})
      </div>

      <div className="flex-1 overflow-y-auto">
        {layers.map((layer, idx) => {
          if (!layer) return null;
          const isVisible = layerVisibility[layer.name] !== false;
          const opacity = layerOpacity[layer.name] ?? 1.0;
          const isDragging = dragIndex === idx;

          return (
            <div
              key={layer.name}
              draggable
              onDragStart={(e) => handleDragStart(e, idx)}
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, idx)}
              className={`flex items-center gap-2 px-2 py-1.5 border-b border-border cursor-move transition-opacity ${
                isDragging ? "opacity-40" : ""
              }`}
            >
              {/* Drag handle */}
              <span className="text-gray-600 text-xs cursor-grab">⠿</span>

              {/* Visibility toggle */}
              <button
                onClick={() => toggleLayerVisibility(layer.name)}
                className={`text-xs w-5 h-5 flex items-center justify-center rounded ${
                  isVisible ? "text-white" : "text-gray-600"
                }`}
                title={isVisible ? "Hide layer" : "Show layer"}
              >
                {isVisible ? "👁" : "⊘"}
              </button>

              {/* Layer name + bone binding */}
              <div className="flex-1 min-w-0">
                <div className="text-xs text-white truncate">{layer.name}</div>
                <div className="text-[9px] text-gray-500 font-mono">{layer.bone}</div>
              </div>

              {/* Opacity slider */}
              <div className="flex items-center gap-1 w-20">
                <input
                  type="range"
                  min={0}
                  max={100}
                  value={Math.round(opacity * 100)}
                  onChange={(e) =>
                    setLayerOpacity(layer.name, parseInt(e.target.value, 10) / 100)
                  }
                  className="w-14 h-1 accent-accent"
                />
                <span className="text-[9px] text-gray-500 w-7 text-right">
                  {Math.round(opacity * 100)}%
                </span>
              </div>

              {/* Z-order indicator */}
              <span className="text-[9px] text-gray-600 w-4 text-center">{layer.z_order}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
