# Receipt Chain Guard — Architecture Specification

**Purpose:** Double-enforcement receipt chain that prevents any pipeline stage from executing when upstream receipts are missing. Enforced at BOTH the Pi Extension level (global) AND per-command (local).

---

## Receipt Dependency Map

```yaml
receipt_chain:
  # Setup Phase Receipts
  H8_soul_values:
    receipt_file: "H8_DISTILLATION_RECEIPT.md"
    receipt_path: "intelligence/soul/"
    required_by: [H10, H3, mirror-session]
    upstream_command: "/ccf-soul-extract"
    
  H10_philosophy_brief:
    receipt_file: "H10_DISTILLATION_RECEIPT.md"
    receipt_path: "intelligence/philosophy/"
    required_by: [H9, H1, H3]
    upstream_command: "/ccf-philosophy-brief"
    
  H11_audience_research:
    receipt_file: "H11_DISTILLATION_RECEIPT.md"
    receipt_path: "intelligence/context_premises/"
    required_by: [H9]
    upstream_command: "/ccf-context-premises"

  H9_tribe_profile:
    receipt_file: "H9_DISTILLATION_RECEIPT.md"
    receipt_path: "intelligence/tribe/"
    required_by: [H12, H13, H5]
    upstream_command: "/ccf-tribe-distill"
    
  # Research Phase Receipts
  H0_layered_questions:
    receipt_file: "H0_DISTILLATION_RECEIPT.md"
    receipt_path: "intelligence/questions/"
    required_by: [H1]
    upstream_command: "/ccf-question-engineer"

  H1_blueprint:
    receipt_file: "H1_DISTILLATION_RECEIPT.md"
    receipt_path: "blueprints/"
    required_by: [H6, H7, H3, soc-generator]
    upstream_command: "/ccf-blueprint"

  H6_deep_research:
    receipt_file: "H6_DISTILLATION_RECEIPT.md"
    receipt_path: "research/deep/"
    required_by: [wisdom-forge]
    upstream_command: "/ccf-deep-research"

  H7_fresh_research:
    receipt_file: "H7_DISTILLATION_RECEIPT.md"
    receipt_path: "research/fresh/"
    required_by: [wisdom-forge]
    upstream_command: "/ccf-fresh-research"

  # Production Phase Receipts
  H3_soc_voice:
    receipt_file: "H3_DISTILLATION_RECEIPT.md"
    receipt_path: "scripts/soc/"
    required_by: [mirror-session, H5]
    upstream_command: "/ccf-soc-generate"

  H14_mirror_session:
    receipt_file: "H14_DISTILLATION_RECEIPT.md"
    receipt_path: "scripts/adapted/"
    required_by: [wisdom-forge]
    upstream_command: "/ccf-adapt"

  H15_wisdom_forge:
    receipt_file: "H15_DISTILLATION_RECEIPT.md"
    receipt_path: "scripts/wisdom/"
    required_by: [script-generator]
    upstream_command: "/ccf-wisdom"

  # Visual Phase Receipts
  H12_visual_recipe:
    receipt_file: "H12_DISTILLATION_RECEIPT.md"
    receipt_path: "visuals/recipes/"
    required_by: [art-director]
    upstream_command: "/ccf-visual-recipe"

  H13_visual_assets:
    receipt_file: "H13_DISTILLATION_RECEIPT.md"
    receipt_path: "visuals/assets/"
    required_by: [H5, art-director]
    upstream_command: "/ccf-visual-assets"
```

---

## Enforcement Layer 1: Per-Command Pre-Flight

Every command file (`commands/ccf-*.md`) MUST include a pre-flight receipt check as Step 1:

```markdown
## STEP 1: PRE-FLIGHT — Receipt Chain Verification

**Before ANY processing begins, verify upstream receipts exist:**

| # | Required Receipt | Path | If Missing |
|:--|:----------------|:-----|:-----------|
| 1 | [upstream receipt] | `{project}/[receipt_path]/[receipt_file]` | ⛔ HALT → Run `[upstream_command]` first |
| 2 | [upstream receipt] | `{project}/[receipt_path]/[receipt_file]` | ⛔ HALT → Run `[upstream_command]` first |

**ALL receipts must exist. Missing ANY receipt = full stop.**

> [!CAUTION]
> Do NOT skip this step. Do NOT proceed with partial receipts.
> A stage that runs without upstream receipts produces output
> that CANNOT be trusted by downstream stages.
```

### Why per-command matters:
- **Immediate feedback** — the agent knows EXACTLY which upstream step is missing
- **Clear routing** — the error message tells the agent which command to run instead
- **No silent failures** — the pipeline halts visibly before producing garbage

---

## Enforcement Layer 2: Pi Extension Guard

The `SystemSelect` or `InteractComp` extension reads the receipt chain YAML and enforces it globally:

```
EXTENSION LOGIC (pseudocode):

on_stage_start(stage_id):
  chain = load_receipt_chain_yaml()
  required_receipts = get_receipts_required_by(stage_id)
  
  for receipt in required_receipts:
    path = resolve_path(receipt.receipt_path, receipt.receipt_file)
    if not file_exists(path):
      HALT_WITH_MESSAGE(
        f"⛔ Cannot proceed with {stage_id}.\n"
        f"Missing upstream receipt: {receipt.receipt_file}\n"
        f"This means {receipt.upstream_command} has not been run or did not pass validation.\n"
        f"Run `{receipt.upstream_command}` first."
      )
    
    # BONUS: Check receipt STATUS
    receipt_content = read_file(path)
    if receipt_content.status == "FAILED":
      HALT_WITH_MESSAGE(
        f"⛔ Upstream receipt {receipt.receipt_file} exists but STATUS = FAILED.\n"
        f"This means {receipt.upstream_command} ran but its output did not pass validation.\n"
        f"Re-run `{receipt.upstream_command}` and fix the failing laws before proceeding."
      )
```

### Why extension-level matters:
- **Catch-all** — even custom flows that skip commands still hit the extension guard
- **FAILED receipt detection** — a receipt that EXISTS but has STATUS = FAILED is caught
- **No code changes per command** — the extension reads a YAML lookup table, not hardcoded logic
- **New stages register automatically** — add a new entry to the YAML, the extension picks it up

---

## Receipt Status Semantics

Every receipt has one of three statuses:

| Status | Meaning | Downstream Behavior |
|:-------|:--------|:-------------------|
| `AUTHENTICATED` | All 4 laws passed, all MH tests passed | ✅ Proceed normally |
| `PROVISIONAL` | 3/4 laws passed, minor gaps flagged | ⚠️ Proceed with caution — downstream stages inherit the flag |
| `FAILED` | ≤2 laws passed, output is unreliable | ⛔ HALT — treat as if receipt doesn't exist |

> [!IMPORTANT]
> A `PROVISIONAL` receipt propagates its flags downstream. If H9 is PROVISIONAL because mode coverage is incomplete, then H12 and H13 receive this flag and must compensate (e.g., by using the interchangeability test fallback instead of the Visual Recognition Code Library).

---

## The Receipt Chain Dependency Graph

```
H8 (Soul Values) ─────────────────────────┐
                                           ↓
H10 (Philosophy Brief) ──→ H9 (Tribe) ──→ H12 (Visual Recipes)
                             ↓              ↓
H11 (Audience Research) ──→ H9            H13 (Visual Assets)
                                           ↓
H0 (Questions) ──→ H1 (Blueprints) ────→ H6 (Deep Research)
                         ↓                 ↓
                         ↓              H7 (Fresh Research)
                         ↓                 ↓
                    H3 (SoC Voice) ────→ H14 (Mirror) ──→ H15 (Wisdom) ──→ Script
                         ↓
                    H5 (Visual Prompts)
```

Every arrow = a receipt requirement. Every node = a receipt producer.
