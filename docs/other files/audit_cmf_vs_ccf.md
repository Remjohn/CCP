# CCF Skills & Commands Reference Matrix for Implementation Docs (H0-H13)

> This matrix maps each implementation doc to the **exact CCF skill and command files** it should reference.
> Any reference NOT in this matrix is either CMF-specific or incorrect.

---

## CCF Pipeline Flow (Correct Routing)

```
SETUP PHASE:
  ccf-soul-extract → setup/client-soul-extraction/SKILL.md
  ccf-tribe-extract → setup/tribe-soul-extraction/SKILL.md

WEEKLY CYCLE:
  1. ccf-radar → content/intelligence-radar/SKILL.md
  2. ccf-question → content/question-engineer/SKILL.md
  3. ccf-theme-discover → content/dynamic-theme-generator/SKILL.md
  4. ccf-research-deep → research/deep-analysts/SKILL.md (×42)
  5. ccf-research-fresh → research/fresh-analysts/SKILL.md (×42)
  6. ccf-blueprint → research/blueprint-orchestrator/SKILL.md
  7. ccf-script → content/script-architect/SKILL.md

PRODUCTION CYCLE (per theme):
  1. ccf-soc → production/soc-generator/SKILL.md
  2. ccf-adapt → (prompt adaptation stage)
  3. ccf-wisdom → production/wisdom-forge/SKILL.md
  4. ccf-generate → production/script-generator/SKILL.md
  5. ccf-validate → validation/critic/SKILL.md

DISTRIBUTION PHASE:
  6. ccf-visual → distribution/art-director/SKILL.md
  7. art-director → distribution/visual-recipes/{archetype}/SKILL.md (×14)
```

---

## Per-H Reference Audit

### H0: Layered Questions
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** Question Engineer | `ccf-26/skills/ccf/content/question-engineer/SKILL.md` | ✅ Referenced in rewritten doc |
| **Command:** ccf-question | `ccf-26/commands/ccf-question.md` | ✅ |
| **Input:** intelligence_radar.json | From `content/intelligence-radar/` | ✅ |
| **Input:** project_context.json | Layer 6 + Layer 7 | ✅ |
| **Output:** provocation_questions.json | CCF weekly output | ✅ |

### H1: Blueprint Orchestrator
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** Blueprint Orchestrator | `ccf-26/skills/ccf/research/blueprint-orchestrator/SKILL.md` | ⚠️ Not explicitly referenced |
| **Skill:** Archetype Mapping | `ccf-26/skills/ccf/research/archetype-mapping/SKILL.md` | ⚠️ Not explicitly referenced |
| **Command:** ccf-blueprint | `ccf-26/commands/ccf-blueprint.md` | ⚠️ Referenced as concept but not by path |
| **Input:** content_blueprints.json | From blueprint orchestrator | ⚠️ Doc says `blueprints.json` |
| **Input:** soul_values.json | From setup/client-soul-extraction | ✅ |
| **Input:** tribe_profile.json | From setup/tribe-soul-extraction | ✅ |
| **Downstream:** SoC Generator | `ccf-26/skills/ccf/production/soc-generator/SKILL.md` | ⚠️ Referenced by name, not path |
| **Issue:** `coach_session_{date}.md` | Should reference `provocation_questions.json` output flow | ❌ Wrong input name |
| **Issue:** "E-Roll-VULNERABILITY" routing | E-Roll is CMF. CCF visual = `art-director` | ❌ CMF reference |

### H2: Deep Research (CMF — correct)
| Should Reference | Actual CMF Path | Status |
|:---|:---|:---|
| Stays CMF per user specification | CMF E-Roll pipeline | ✅ No changes |

### H3: SoC Generator (Voice)
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** SoC Generator v4 | `ccf-26/skills/ccf/production/soc-generator/SKILL.md` | ⚠️ Referenced by name, not path |
| **Command:** ccf-soc | `ccf-26/commands/ccf-soc.md` | ⚠️ Not referenced |
| **Input:** content_blueprints.json | `downstream_routing` field | ✅ concept correct |
| **Input:** soul_values.json | From setup | ✅ |
| **Input:** context_premise_spr.md | From content phase | ✅ |
| **Input:** coach_soc_batch.md | Coach recorded moments | ✅ |
| **Input:** vibe_comments_processed.json | From vibe comments | ✅ |
| **Output:** soc_output.json | `scripts/soc/{blueprint_id}_soc_output.json` | ⚠️ Doc says `{blueprint_id}_soc_output.json` (close) |
| **Issue:** Line 13 says "CMF pipeline" | Should say "CCF pipeline" | ❌ |
| **Issue:** "Script-Adapter → Witness arc tone" | Should reference `production/script-generator` or `content/script-architect` | ❌ Mixed CMF |
| **Issue:** "CLEARED FOR SCRIPT ADAPTATION" | Should name CCF subsystem | ❌ |

### H4: E-Roll Visual Search → CCF Visual Pipeline
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** Art Director | `ccf-26/skills/ccf/distribution/art-director/SKILL.md` | ❌ Not referenced — uses "E-Roll" |
| **Skill:** Visual Recipes (×14) | `ccf-26/skills/ccf/distribution/visual-recipes/*/SKILL.md` | ❌ Not referenced |
| **Command:** ccf-visual | `commands/ccf-visual.md` | ❌ Not referenced |
| **Command:** ccf-eroll-research | `commands/ccf-eroll-research.md` | ⚠️ This IS CCF (eroll research exists in commands/) |
| **Issue:** Entire doc framed around CMF E-Roll concept | Needs significant reframing for CCF visual pipeline | ❌ Major |
| **Issue:** "CMF Phase 1b" | Should say CCF Distribution Phase | ❌ |
| **Issue:** "Storyboard Composer" (×3) | CCF = "Art Director" | ❌ |
| **Issue:** "CLEARED FOR STORYBOARD GENERATION (H5)" | Should reference CCF visual distribution | ❌ |

### H5: Visual Prompt Writing → CCF Visual Recipes
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** Visual Recipes | `ccf-26/skills/ccf/distribution/visual-recipes/*/SKILL.md` | ❌ Not referenced by path |
| **Skill:** Art Director | `ccf-26/skills/ccf/distribution/art-director/SKILL.md` | ❌ Not referenced |
| **Command:** ccf-visual | `commands/ccf-visual.md` | ❌ Not referenced |
| **Input:** final script | `scripts/final/{blueprint_id}_script.md` | ⚠️ Doc says `final_script.json` (wrong ext) |
| **Input:** soul_values.json | From setup | ✅ |
| **Issue:** "CMF Phase 1b" | Should say CCF Distribution Phase | ❌ |
| **Issue:** "Storyboard Composer" | CCF = "Art Director + Visual Recipes" | ❌ |
| **Issue:** "CMF Distillation Funnel" (×2) | Should say "CCF" | ❌ |

### H6: RAW Deep Research
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** Deep Analysts (42 skills) | `ccf-26/skills/ccf/research/deep-analysts/*/SKILL.md` | ✅ |
| **Skill:** _DEEP_RESEARCH_PROTOCOL | `ccf-26/skills/ccf/research/deep-analysts/_DEEP_RESEARCH_PROTOCOL.md` | ✅ |
| **Command:** ccf-research-deep | `ccf-26/commands/ccf-research-deep.md` | ✅ |

### H7: RAW Fresh Research
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** Fresh Analysts (42 skills) | `ccf-26/skills/ccf/research/fresh-analysts/*/SKILL.md` | ✅ |
| **Command:** ccf-research-fresh | `ccf-26/commands/ccf-research-fresh.md` | ✅ |

### H8: Coach Soul Values
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** Client Soul Extraction | `ccf-26/skills/ccf/setup/client-soul-extraction/SKILL.md` | ✅ |
| **Command:** ccf-soul-extract | `ccf-26/commands/ccf-soul-extract.md` | ✅ |

### H9: Soul Tribe Profiles
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** Tribe Soul Extraction | `ccf-26/skills/ccf/setup/tribe-soul-extraction/SKILL.md` | ✅ |
| **Command:** ccf-tribe-extract | `ccf-26/commands/ccf-tribe-extract.md` | ✅ |

### H10: Coach Philosophy Brief
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** Client Soul Extraction | `ccf-26/skills/ccf/setup/client-soul-extraction/SKILL.md` | ✅ |
| **Command:** ccf-soul-extract | `ccf-26/commands/ccf-soul-extract.md` | ✅ |

### H11: Raw Target Audience Research
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** Tribe Soul Extraction | `ccf-26/skills/ccf/setup/tribe-soul-extraction/SKILL.md` | ✅ |
| **Command:** ccf-tribe-extract | `ccf-26/commands/ccf-tribe-extract.md` | ✅ |

### H12: Visual Recipe Distillation
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| **Skill:** Visual Recipes (14 skills) | `ccf-26/skills/ccf/distribution/visual-recipes/*/SKILL.md` | ✅ |
| **Skill:** Art Director | `ccf-26/skills/ccf/distribution/art-director/SKILL.md` | ✅ |

### H13: Standalone Visual Asset Research
| Should Reference | Actual CCF Path | Status |
|:---|:---|:---|
| New skill — no existing infrastructure | Proposed: `ccf-26/skills/ccf/distribution/visual-asset-researcher/SKILL.md` | ✅ (new) |

---

## Summary: What Needs Fixing

| Doc | Errors | Severity |
|:---|:---|:---|
| **H0** | ✅ Already fixed | Done |
| **H1** | 3 errors: wrong input name, E-Roll routing, missing skill paths | Medium |
| **H2** | ✅ CMF correct | Done |
| **H3** | 3 errors: "CMF pipeline", Script-Adapter routing, clearance name | Low–Medium |
| **H4** | 6 errors: entire E-Roll framing, CMF Phase 1b, Storyboard (×3), clearance | **High** |
| **H5** | 5 errors: CMF Phase 1b, Storyboard, CMF Funnel (×2), wrong file ext | **High** |
| **H6–H13** | ✅ All correct | Done |
