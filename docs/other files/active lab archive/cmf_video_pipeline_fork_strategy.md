# CMF Video Pipeline: Fork Strategy & B-Roll Fingerprint Architecture

## The 3 Repos — Side-by-Side Comparison

| | **Video Wizard** | **AI-Youtube-Shorts-Generator** | **YT-Short-Clipper** |
|---|---|---|---|
| **Core Purpose** | Create & render videos with Remotion | Extract highlights from existing YouTube videos | Clip & reformat YouTube podcasts/interviews |
| **Tech Stack** | Next.js 16 + Remotion + FastAPI + Whisper | Python + FFmpeg + GPT-4 + OpenCV | Python + FFmpeg + GPT-4 + Whisper |
| **Remotion?** | ✅ Full Remotion Studio + render server | ❌ FFmpeg only | ❌ FFmpeg only |
| **Caption System** | ✅ 9 professional templates (hormozi, mrbeast, viral, etc.) | Basic Franklin Gothic burn-in | CapCut-style word-by-word |
| **Architecture** | Monorepo (web + remotion-server + processing-engine) | Single Python script | Single Python app + Streamlit GUI |
| **Creation vs Repurposing** | **Creation** pipeline (upload assets → compose → render) | **Repurposing** (YouTube URL → extract clip) | **Repurposing** (YouTube URL → clip → reformat) |
| **Smart Crop** | ✅ AI face detection (MediaPipe) + 9:16 | ✅ Face + screen recording modes | ✅ OpenCV + MediaPipe speaker tracking |
| **Whisper Integration** | ✅ Python Whisper + timing sync | ✅ GPU-accelerated Whisper | ✅ Whisper + word-level timestamps |
| **Render Queue** | ✅ Express job queue with progress tracking | ❌ Sequential | ❌ Sequential |
| **Stars** | ~50 | ~2,400+ | ~200+ |
| **Last Updated** | Feb 2026 | Active | Active |

---

## Verdict: Fork Video Wizard, Cherry-Pick From the Other Two

### Why Video Wizard Is Your Base

1. **It's a creation tool, not a repurposing tool.** The other two repos take an existing YouTube video and extract clips. CMF doesn't have YouTube videos to clip — CMF creates videos from scratch using generated images, voiceover, and music. Video Wizard's architecture matches this: upload assets → compose → render.

2. **Remotion is already integrated.** Full Remotion Studio, a dedicated render server with job queue, and 9 caption templates. This is exactly the infrastructure my feasibility analysis recommended — and it's already built.

3. **Monorepo architecture.** Three cleanly separated apps:
   - `apps/web/` — Next.js frontend (review UI)
   - `apps/remotion-server/` — Express + Remotion (render engine)
   - `apps/processing-engine/` — FastAPI Python (Whisper, FFmpeg, face detection)
   
   CMF can add a 4th app for its specific assembly logic without touching the existing code.

4. **FastAPI processing engine.** Already has Whisper transcription, FFmpeg rendering, audio extraction — the exact audio pipeline CMF needs.

### What To Cherry-Pick From the Others

| Feature | Source Repo | Why Take It |
|---------|-------------|-------------|
| **CapCut-style word-by-word captions** | YT-Short-Clipper | More dynamic than Video Wizard's sentence-level templates; CMF's fast-paced style needs word-level punch |
| **Hook generation with TTS overlay** | YT-Short-Clipper | AI-generated text intro scenes — useful for CMF's opening hook beats |
| **Concurrent session execution** | AI-Youtube-Shorts-Generator | Unique session IDs allow parallel batch processing — essential for 8-12 videos/day |
| **Auto-approve timeout workflow** | AI-Youtube-Shorts-Generator | 15-second auto-approve pattern enables batch pipeline without blocking on every video |
| **SEO metadata generation** | YT-Short-Clipper | AI-optimized titles/descriptions for each rendered video |

---

## The Complete Pipeline: T2I → I2V → Remotion

### What Changes with RunningHub I2V

The original architecture assumed static images per beat. With RunningHub handling both **text-to-image** (T2I) AND **image-to-video** (I2V), each beat produces a **video clip**, not a still frame. This fundamentally upgrades the output quality — instead of a slideshow with transitions, CMF produces actual cinematic motion per beat.

```
CMF GENERATION PIPELINE (per beat):

Beat Cluster   Storyboard     RunningHub        RunningHub        Remotion
 (timing)  →→  Composer   →→   T2I Workflow  →→  I2V Workflow  →→  Assembly
              (prompt)        (still image)     (video clip)      (timeline)
                                   │                  │
                                   ▼                  ▼
                              fingerprint         fingerprint
                              stage_1             stage_2
                              (T2I params)        (I2V params)
```

**Stage 1 — T2I (Text-to-Image):**
- Input: Visual prompt from storyboard composer + PSSL parameters
- RunningHub workflow: ComfyUI T2I workflow (SDXL, Flux, etc.)
- Output: High-resolution still image (keyframe)
- API: `https://www.runninghub.ai/proxy/{api-key}` or `/proxy-plus/{api-key}` (48GB)

**Stage 2 — I2V (Image-to-Video):**
- Input: Stage 1 keyframe image + motion parameters
- RunningHub workflow: ComfyUI I2V workflow (AnimateDiff, SVD, etc.)
- Output: 3-5 second video clip per beat
- API: Same RunningHub proxy, different workflow ID
- Uses the plugin's 5 independent video output ports for batch processing

**Stage 3 — Remotion Assembly:**
- Input: All beat video clips + voiceover + music + captions
- Remotion `<Video>` components (not `<Img>`) per beat
- Transitions between beat clips (not between static images)
- Output: Complete 60-second video ready for review

### RunningHub API Integration Pattern

The RunningHub ComfyUI API functions identically to a local ComfyUI deployment. The CMF assembler communicates via:

```
┌──────────────────────────┐
│  CMF Assembler            │
│                           │
│  POST workflow to         │
│  RunningHub Proxy         │──────▶ RunningHub Cloud GPU
│                           │        (24GB or 48GB VRAM)
│  WebSocket / HTTP Poll    │◀────── Progress + Status
│  for job monitoring       │
│                           │
│  Download output from     │◀────── Video/Image/Audio
│  5 video output ports     │        output endpoints
└──────────────────────────┘
```

Key API capabilities (from `ComfyUI_RH_APICall` plugin):
- **Input support:** video, audio, image file upload
- **Output support:** images, video frames, latent, text, audio files
- **5 independent video output ports** — parallel beat generation
- **WebSocket + HTTP polling** fallback for job monitoring
- **Progress bar** feedback for long-running I2V tasks
- **NodeInfoList** node can modify any workflow parameter (prompt, seed, batch size)

---

## Dual-Stage Fingerprint Architecture

### Why Two Stages

With T2I → I2V, the fingerprint must track **both** generation steps independently. If the operator likes the keyframe image but not the motion, they should regenerate ONLY the I2V stage. If they dislike the image itself, they regenerate T2I (which cascades to a new I2V).

### Fingerprint Schema (Updated for I2V)

```json
{
  "video_id": "CMF-VID-20260321-001",
  "beat_cluster_id": "BC-WITNESS-42",
  "beats": [
    {
      "beat_index": 0,
      "beat_type": "hook",
      "duration_sec": 4.2,
      "fingerprint": {
        "fingerprint_id": "FP-VID-20260321-001-B0",
        
        "stage_1_t2i": {
          "status": "GENERATED",
          "runninghub_workflow_id": "RH-WF-CMF-T2I-FLUX-001",
          "prompt_used": "Close-up of hands gripping a weathered leather journal, dim amber light, shallow depth of field...",
          "negative_prompt": "blurry, generic, stock photo, smooth skin, text",
          "visual_prompt_source": "storyboard-composer output beat 0",
          "seed": 42891,
          "model": "flux-dev-fp8",
          "pssl_params": {
            "foundation_hue": "#2C3E50",
            "temperature": "warm",
            "spatial_density": 7,
            "pad_scores": {"P": 0.3, "A": 0.8, "D": 0.4}
          },
          "output_image_url": "https://r2.cmf-assets.com/t2i/fp-001-b0-keyframe.png",
          "generation_timestamp": "2026-03-21T02:15:00Z"
        },
        
        "stage_2_i2v": {
          "status": "GENERATED",
          "runninghub_workflow_id": "RH-WF-CMF-I2V-SVD-001",
          "input_image_url": "https://r2.cmf-assets.com/t2i/fp-001-b0-keyframe.png",
          "motion_parameters": {
            "motion_bucket_id": 127,
            "fps": 24,
            "duration_frames": 96,
            "motion_strength": 0.6,
            "camera_motion": "slow_zoom_in"
          },
          "output_video_url": "https://r2.cmf-assets.com/i2v/fp-001-b0-clip.mp4",
          "generation_timestamp": "2026-03-21T02:16:30Z"
        }
      },
      "regeneration_history": []
    }
  ]
}
```

### Three Regeneration Modes

```
┌─────────────────────────────────────────────────────────┐
│  REMOTION PREVIEW (Browser)                              │
│                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                │
│  │ Beat 0   │ │ Beat 1   │ │ Beat 2   │  ...           │
│  │ [▶ clip] │ │ [▶ clip] │ │ [▶ clip] │                │
│  │          │ │          │ │          │                │
│  │ [🖼️ T2I] │ │ [✅]     │ │ [🎬 I2V] │                │
│  │ [🎬 I2V] │ │          │ │          │                │
│  │ [🔄 Both]│ │          │ │ [🔄 Both]│                │
│  └──────────┘ └──────────┘ └──────────┘                │
│                                                          │
│  🖼️ = Regenerate keyframe only (T2I) → auto-reruns I2V  │
│  🎬 = Regenerate motion only (I2V) — keep same keyframe │
│  🔄 = Regenerate both stages from scratch                │
└─────────────────────────────────────────────────────────┘
```

| Action | What Happens | When To Use |
|--------|-------------|-------------|
| **🖼️ Regen T2I** | New keyframe → automatically triggers new I2V | Image content is wrong (wrong scene, wrong framing) |
| **🎬 Regen I2V** | Same keyframe → new motion/animation | Image is good but motion is wrong (jitter, wrong camera move) |
| **🔄 Regen Both** | Full re-generation from prompt | Everything needs to change |

---

## Proposed Architecture (Updated for I2V)

```
┌────────────────────────────────────────────────────────────────┐
│                     FORKED VIDEO WIZARD                         │
│                                                                 │
│  apps/web/              → Review UI + 3-mode beat regeneration  │
│  apps/remotion-server/  → Render queue + CMF <Video> templates  │
│  apps/processing-engine/ → Whisper + FFmpeg + Demucs            │
│                                                                 │
│  apps/cmf-assembler/    → NEW: CMF-specific assembly layer      │
│    ├── beat_cluster_parser.py    (parse beat cluster JSON)       │
│    ├── runninghub_client.py      (T2I + I2V API orchestration)  │
│    ├── timeline_generator.ts     (Remotion video manifest)      │
│    ├── fingerprint_tracker.py    (dual-stage provenance)        │
│    ├── audio_engine.py           (ducking, stems, sync)         │
│    └── regeneration_handler.py   (3-mode beat re-gen)           │
│                                                                 │
│  packages/remotion-compositions/                                │
│    └── src/templates/                                           │
│        ├── cmf-witness.tsx       (Witness arc — Video clips)    │
│        ├── cmf-breakthrough.tsx  (Breakthrough arc)             │
│        └── ...                   (one per arc type)             │
│                                                                 │
│  Key Difference: Remotion uses <Video> not <Img> per beat       │
│  Key Difference: runninghub_client handles 2-stage generation   │
│  Key Difference: Fingerprint has stage_1_t2i + stage_2_i2v      │
└────────────────────────────────────────────────────────────────┘
```

### The Critical New Module: `runninghub_client.py`

This is the bridge between CMF's visual prompts and RunningHub's ComfyUI API:

```python
# Pseudocode — runninghub_client.py

class RunningHubClient:
    BASE_URL = "https://www.runninghub.ai/proxy/{api_key}"      # 24GB
    PLUS_URL = "https://www.runninghub.ai/proxy-plus/{api_key}"  # 48GB (for I2V)

    async def generate_beat(self, beat, visual_prompt, pssl_params):
        # Stage 1: T2I
        t2i_workflow = load_workflow("RH-WF-CMF-T2I-FLUX-001")
        t2i_workflow.set_node("prompt", visual_prompt)
        t2i_workflow.set_node("negative_prompt", pssl_params.negative)
        t2i_workflow.set_node("seed", random_seed())
        
        keyframe = await self.submit_and_wait(t2i_workflow)
        # → Returns image URL
        
        # Stage 2: I2V
        i2v_workflow = load_workflow("RH-WF-CMF-I2V-SVD-001")
        i2v_workflow.set_node("input_image", keyframe.image_url)
        i2v_workflow.set_node("motion_bucket_id", 127)
        i2v_workflow.set_node("fps", 24)
        i2v_workflow.set_node("frames", beat.duration_sec * 24)
        
        video_clip = await self.submit_and_wait(i2v_workflow)
        # → Returns video URL from one of 5 output ports
        
        return BeatFingerprint(
            stage_1_t2i=keyframe.metadata,
            stage_2_i2v=video_clip.metadata
        )
    
    async def regenerate_t2i_only(self, fingerprint, revision_note):
        # Re-run T2I with enhanced prompt, then cascade to I2V
        ...
    
    async def regenerate_i2v_only(self, fingerprint, motion_params):
        # Re-run I2V with same keyframe but different motion
        ...
```

### How Remotion Compositions Change

With video clips instead of static images, the Remotion template shifts from `<Img>` to `<Video>`:

```tsx
// cmf-witness.tsx (simplified)
import { Video, Sequence, useVideoConfig } from "remotion";

export const CMFWitnessArc: React.FC<{ manifest: CMFManifest }> = ({ manifest }) => {
  const { fps } = useVideoConfig();
  
  return (
    <>
      {manifest.beats.map((beat, i) => (
        <Sequence
          key={i}
          from={beat.startFrame}
          durationInFrames={beat.durationFrames}
        >
          {/* Each beat is a VIDEO CLIP, not a static image */}
          <Video
            src={beat.fingerprint.stage_2_i2v.output_video_url}
            style={{ width: "100%", height: "100%" }}
          />
          
          {/* Captions overlay on top of video */}
          <WordByWordCaption
            words={beat.caption_words}
            style="hormozi"
          />
        </Sequence>
      ))}
      
      {/* Audio layers */}
      <Audio src={manifest.voiceover_url} />
      <Audio src={manifest.music_url} volume={manifest.ducking_curve} />
    </>
  );
};
```

---

## Build Plan (Revised for T2I → I2V Pipeline)

### Phase 0: Fork & Strip (Day 1)
- Fork `el-frontend/video-wizard` to your repo
- Strip: content intelligence, viral scoring, video upload flow
- Keep: Remotion server, processing engine, web skeleton, caption templates

### Phase 1: RunningHub Client + CMF Assembler (Days 2-5)
- Build `runninghub_client.py` — T2I + I2V orchestration via RunningHub proxy API
- Build beat cluster parser → generates generation jobs per beat
- Build fingerprint tracker (dual-stage: `stage_1_t2i` + `stage_2_i2v`)
- Build timeline generator → Remotion JSON manifest with video clip URLs
- Integrate WebSocket/HTTP polling for job progress monitoring
- Audio engine (Whisper STT, Demucs stems, sidechain ducking)

### Phase 2: Remotion Video Templates (Days 6-7)
- Create `<Video>`-based Remotion compositions per arc type (start with Witness)
- Transition presets between video clips (crossfade, cut-to-beat, zoom transitions)
- Caption template (word-by-word cherry-picked from YT-Short-Clipper)
- Audio ducking curve integration

### Phase 3: Review UI + 3-Mode Regeneration (Days 8-10)
- Modify web app for beat-level video review
- Three regeneration buttons per beat: 🖼️ T2I only, 🎬 I2V only, 🔄 Both
- Revision note popup → enhanced prompt or motion param adjustment
- Approve / regenerate / edit workflow (mirrors CVE's FR-VIS-05)
- Batch auto-approve for high-confidence beats

### Phase 4: Pipeline Integration (Days 11-12)
- Wire into CMF commander flow
- End-to-end test: beat cluster → T2I → I2V → assembled video → review → render
- Parallel beat generation (all beats concurrently via RunningHub's concurrent task mode)
- Document the skill for CMF agent consumption

**Total: ~12 days**

---

## CVE Patterns Worth Porting to CMF

| CVE Pattern | CMF Application |
|---|---|
| **4-tier sourcing cascade** | B-roll library → stock video API → RunningHub T2I+I2V |
| **Parallel slide processing** | Generate all beats concurrently via RunningHub's 5 video output ports |
| **Adequacy threshold (0.7)** | Score generated keyframes against visual prompt; auto-flag low scores before I2V |
| **Dual-stage fingerprint** | Track T2I and I2V independently for surgical regeneration |
| **Status machine** | `GENERATING_T2I → GENERATING_I2V → ASSEMBLING → READY_FOR_REVIEW → APPROVED` |
| **Request Regeneration** | 3-mode regeneration (T2I only, I2V only, or both) with revision notes |

> [!IMPORTANT]
> **Gate between T2I and I2V:** Before sending a keyframe to the I2V workflow, the system should auto-score the keyframe against PSSL parameters (like CVE's adequacy threshold). If the keyframe scores below 0.6, auto-regenerate T2I with enhanced specificity BEFORE wasting GPU time on I2V. This saves significant compute cost.
