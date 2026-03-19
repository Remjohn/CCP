# FR Prompts — CCP Updates

## Active Prompts

| Prompt | File | Purpose |
|---|---|---|
| **Spec Audit** | [PROMPT_Spec_Audit.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/PROMPT_Spec_Audit.md) | 5-lens review of a spec batch — produces flagged findings |
| **Spec Revision** | [PROMPT_Spec_Revision.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/PROMPT_Spec_Revision.md) | Takes audit findings → produces copy-pasteable fix instructions |

## Workflow

1. Write all specs in a batch
2. Run **Spec Audit** prompt → get Audit Report with flags
3. Review flags, make architect decisions on any that require arbitration
4. Run **Spec Revision** prompt with the Audit Report → get executable fix instructions
5. Apply fixes to specs

## Previously Completed

- **FR1-9:** Audited + Revised ✅
- **FR10-19:** Audited + Revised ✅
- **FR20-29:** Audited + Revised ✅
- **FR30-39:** Audited + Revised ✅
- **FR40-50:** Audited + Revised ✅

## Pending Audit

- **Batch A — FR-CBCS-01 through CBCS-14** (14 specs)
- **Batch B — FR51 through FR60** (10 specs)
- **Batch C — FR-VIS-01 through VIS-13** (13 specs)
