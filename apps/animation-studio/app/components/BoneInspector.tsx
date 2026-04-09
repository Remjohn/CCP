"use client";

// =============================================================================
// FR-VID-13 §4 Stage 5 — Bone Inspector Panel
// Features: numerical inputs (rotation, x, y, scale), keyframe set/clear/reset,
//           bone hierarchy tree (collapsible)
// Spec Reference: §4 Stage 5 Steps 1-4
// =============================================================================

import React, { useState } from "react";
import { useStudioStore } from "../store";

// 15-bone CCP Canonical Skeleton hierarchy from §4 Stage 5 Step 2
interface BoneNode {
  name: string;
  children: BoneNode[];
}

const BONE_HIERARCHY: BoneNode = {
  name: "b_root",
  children: [
    {
      name: "b_hips",
      children: [
        {
          name: "b_leg_upper_L",
          children: [
            { name: "b_leg_lower_L", children: [{ name: "b_foot_L", children: [] }] },
          ],
        },
        {
          name: "b_leg_upper_R",
          children: [
            { name: "b_leg_lower_R", children: [{ name: "b_foot_R", children: [] }] },
          ],
        },
        {
          name: "b_chest",
          children: [
            {
              name: "b_arm_upper_L",
              children: [
                {
                  name: "b_arm_lower_L",
                  children: [{ name: "b_hand_L", children: [] }],
                },
              ],
            },
            {
              name: "b_arm_upper_R",
              children: [
                {
                  name: "b_arm_lower_R",
                  children: [{ name: "b_hand_R", children: [] }],
                },
              ],
            },
            {
              name: "b_neck",
              children: [
                {
                  name: "b_head",
                  children: [
                    { name: "b_eye_L", children: [] },
                    { name: "b_eye_R", children: [] },
                    { name: "b_jaw", children: [] },
                    { name: "b_hair_front", children: [] },
                    { name: "b_hair_back", children: [] },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
  ],
};

function BoneTreeNode({
  node,
  depth,
  selectedBone,
  onSelect,
}: {
  node: BoneNode;
  depth: number;
  selectedBone: string | null;
  onSelect: (name: string) => void;
}) {
  const [expanded, setExpanded] = useState(depth < 3);
  const hasChildren = node.children.length > 0;
  const isSelected = selectedBone === node.name;

  return (
    <div>
      <div
        className={`flex items-center gap-1 px-1 py-0.5 cursor-pointer rounded text-xs transition-colors ${
          isSelected ? "bg-accent/30 text-white" : "text-gray-400 hover:text-white hover:bg-[#333]"
        }`}
        style={{ paddingLeft: depth * 12 + 4 }}
        onClick={() => onSelect(node.name)}
      >
        {hasChildren && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              setExpanded(!expanded);
            }}
            className="w-3 text-[10px] text-gray-500 hover:text-white"
          >
            {expanded ? "▼" : "▶"}
          </button>
        )}
        {!hasChildren && <span className="w-3" />}
        <span className="font-mono text-[11px]">{node.name}</span>
      </div>
      {expanded &&
        node.children.map((child) => (
          <BoneTreeNode
            key={child.name}
            node={child}
            depth={depth + 1}
            selectedBone={selectedBone}
            onSelect={onSelect}
          />
        ))}
    </div>
  );
}

export function BoneInspector() {
  const selectedBone = useStudioStore((s) => s.selectedBone);
  const selectBone = useStudioStore((s) => s.selectBone);
  const selectedBeatIndex = useStudioStore((s) => s.selectedBeatIndex);
  const currentFrame = useStudioStore((s) => s.currentFrame);
  const manifest = useStudioStore((s) => s.manifest);
  const setBoneKeyframe = useStudioStore((s) => s.setBoneKeyframe);
  const clearBoneKeyframe = useStudioStore((s) => s.clearBoneKeyframe);
  const resetBoneOverrides = useStudioStore((s) => s.resetBoneOverrides);
  const characterPackage = useStudioStore((s) => s.characterPackage);

  // Get current bone data from skeleton
  const boneData = characterPackage?.skeleton.bones.find((b) => b.name === selectedBone);

  // Get current overrides for this bone on this beat
  const beat = manifest?.beats[selectedBeatIndex];
  const overrides = beat?.character_overlay?.bone_overrides?.[selectedBone ?? ""] ?? [];
  const currentOverride = overrides.find((kf) => kf.frame === currentFrame);

  const [rotationInput, setRotationInput] = useState<string>(
    String(currentOverride?.rotation ?? boneData?.rotation ?? 0)
  );
  const [xInput, setXInput] = useState<string>(String(boneData?.x ?? 0));
  const [yInput, setYInput] = useState<string>(String(boneData?.y ?? 0));
  const [scaleInput, setScaleInput] = useState<string>("1.0");

  function handleSetKeyframe() {
    if (!selectedBone) return;
    const rotation = parseFloat(rotationInput);
    if (isNaN(rotation) || rotation < -180 || rotation > 180) return;
    setBoneKeyframe(selectedBeatIndex, selectedBone, currentFrame, rotation);
  }

  function handleClearKeyframe() {
    if (!selectedBone) return;
    clearBoneKeyframe(selectedBeatIndex, selectedBone, currentFrame);
  }

  function handleResetToDefault() {
    if (!selectedBone) return;
    resetBoneOverrides(selectedBeatIndex, selectedBone);
  }

  // Find parent bone name
  function findParent(node: BoneNode, target: string): string | null {
    for (const child of node.children) {
      if (child.name === target) return node.name;
      const found = findParent(child, target);
      if (found) return found;
    }
    return null;
  }

  function findChildren(node: BoneNode, target: string): string[] {
    if (node.name === target) return node.children.map((c) => c.name);
    for (const child of node.children) {
      const found = findChildren(child, target);
      if (found.length > 0) return found;
    }
    return [];
  }

  const parentBone = selectedBone ? findParent(BONE_HIERARCHY, selectedBone) : null;
  const childBones = selectedBone ? findChildren(BONE_HIERARCHY, selectedBone) : [];

  return (
    <div className="flex flex-col h-full">
      {/* Bone Hierarchy Tree */}
      <div className="flex-1 overflow-y-auto border-b border-border p-1">
        <div className="text-[10px] font-bold text-gray-400 uppercase mb-1 px-1">Bone Hierarchy</div>
        <BoneTreeNode
          node={BONE_HIERARCHY}
          depth={0}
          selectedBone={selectedBone}
          onSelect={selectBone}
        />
      </div>

      {/* Inspector Panel */}
      <div className="p-2 space-y-2">
        <div className="text-[10px] font-bold text-gray-400 uppercase">Bone Inspector</div>

        {!selectedBone ? (
          <div className="text-xs text-gray-500">Select a bone to inspect.</div>
        ) : (
          <>
            {/* Bone Info */}
            <div className="text-xs text-white font-mono">{selectedBone}</div>
            {parentBone && (
              <div className="text-[10px] text-gray-500">Parent: {parentBone}</div>
            )}
            {childBones.length > 0 && (
              <div className="text-[10px] text-gray-500">
                Children: {childBones.join(", ")}
              </div>
            )}

            {/* Rotation — ±180° */}
            <div className="flex items-center gap-2">
              <label className="text-[10px] text-gray-400 w-14">Rotation</label>
              <input
                type="number"
                min={-180}
                max={180}
                step={0.5}
                value={rotationInput}
                onChange={(e) => setRotationInput(e.target.value)}
                className="flex-1 bg-[#1a1a1a] border border-border rounded px-1.5 py-0.5 text-xs text-white w-16"
              />
              <span className="text-[10px] text-gray-500">°</span>
            </div>

            {/* X Offset */}
            <div className="flex items-center gap-2">
              <label className="text-[10px] text-gray-400 w-14">X Offset</label>
              <input
                type="number"
                step={1}
                value={xInput}
                onChange={(e) => setXInput(e.target.value)}
                className="flex-1 bg-[#1a1a1a] border border-border rounded px-1.5 py-0.5 text-xs text-white w-16"
              />
              <span className="text-[10px] text-gray-500">px</span>
            </div>

            {/* Y Offset */}
            <div className="flex items-center gap-2">
              <label className="text-[10px] text-gray-400 w-14">Y Offset</label>
              <input
                type="number"
                step={1}
                value={yInput}
                onChange={(e) => setYInput(e.target.value)}
                className="flex-1 bg-[#1a1a1a] border border-border rounded px-1.5 py-0.5 text-xs text-white w-16"
              />
              <span className="text-[10px] text-gray-500">px</span>
            </div>

            {/* Scale — 0.1x to 3.0x */}
            <div className="flex items-center gap-2">
              <label className="text-[10px] text-gray-400 w-14">Scale</label>
              <input
                type="number"
                min={0.1}
                max={3.0}
                step={0.05}
                value={scaleInput}
                onChange={(e) => setScaleInput(e.target.value)}
                className="flex-1 bg-[#1a1a1a] border border-border rounded px-1.5 py-0.5 text-xs text-white w-16"
              />
              <span className="text-[10px] text-gray-500">×</span>
            </div>

            {/* Frame indicator */}
            <div className="text-[10px] text-gray-500">
              Frame: {currentFrame} · Beat: {selectedBeatIndex}
              {currentOverride && (
                <span className="text-yellow-400 ml-1">● keyframe set</span>
              )}
            </div>

            {/* Keyframe actions */}
            <div className="flex gap-1">
              <button
                onClick={handleSetKeyframe}
                className="flex-1 text-[10px] bg-accent hover:bg-accent/80 text-white px-2 py-1 rounded transition-colors"
              >
                Set Keyframe
              </button>
              <button
                onClick={handleClearKeyframe}
                className="flex-1 text-[10px] bg-[#333] hover:bg-[#444] text-gray-300 px-2 py-1 rounded transition-colors"
              >
                Clear
              </button>
              <button
                onClick={handleResetToDefault}
                className="flex-1 text-[10px] bg-red-900/50 hover:bg-red-900/70 text-red-300 px-2 py-1 rounded transition-colors"
              >
                Reset
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
