# CMF V13 Obsolete Files List

## Files to REMOVE (No longer used in V13 pipeline)

### 1. Natron Effects Library (OBSOLETE)
**Reason:** User confirmed Natron effects cannot be properly automated.

```
CMF labo/natron_effects_library/
├── README.md
├── __init__.py
├── cmf_integration.py
├── color_effects.py
├── motion_effects.py
└── transition_effects.py
```

---

### 2. Duplicate/Outdated Virtual Director Versions
**Keep only:** `🌞🎵 The Virtual Director & Storyboard Architect - Song-First Edition.md`

**Remove:**
```
🇫🇷 Conscious Movie Factory/intelligence/guides/
├── 🌞 The Virtual Director & Storyboard Architect.md          ← OLD VERSION
└── 🎬 The Virtual Director & Storyboard Architect - Script-First Edition.md  ← OLD VERSION
```

---

### 3. Outdated Research Generators (E-roll is now searched online)
**Remove:**
```
🇫🇷 Conscious Movie Factory/intelligence/guides/
├── 🔮 D-Roll Research Planning Generator.md  ← D-roll is now coach assets
└── 🔮 E-Roll Research Planning Generator.md  ← E-roll is now searched online
```

---

### 4. RunningHub Pipeline Files (Replaced by manual workflow)
**Remove:**
```
🇫🇷 Conscious Movie Factory/pipeline/
├── config.py
├── runninghub_client.py
├── visual_pipeline_orchestrator.py
└── test_pipeline.py
```

---

### 5. Unused ComfyUI Integration
**Remove:**
```
CMF labo/comfyui_qwen_runninghub/  ← Entire folder (manual workflow instead)
```

---

## Files to KEEP (Essential for V13)

| File | Purpose |
|------|---------|
| `Virtual Director - Song-First Edition.md` | Generate T2I + I2V prompts |
| `AI Video Creation Guide.md` | Qwen prompting reference |
| `director_console/` | Streamlit UI |
| `Z-Image Turbo BF16_api.json` | RunningHub workflow ref |
| `Wan 2.2 i2v Strong dynamics_api.json` | RunningHub workflow ref |
| `wanvideo_1_3B_FlashVSR_upscale_api.json` | RunningHub workflow ref |
| `scene_cutter.py` | FFmpeg A-roll cutting |

---

## Summary

| Category | Files to Remove |
|----------|-----------------|
| Natron library | 6 files |
| Old Virtual Directors | 2 files |
| Old Research Generators | 2 files |
| Pipeline code | 4 files |
| ComfyUI folder | ~10 files |
| **Total** | **~24 files** |

**Disk space saved:** Approximately 100-200 KB (mostly documentation)
