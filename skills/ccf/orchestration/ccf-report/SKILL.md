---
name: "Production Dashboard"
description: "Displays batch production metrics and quality summary"
session_id: ccf-report
phase: reporting
ccp_layer: Monitoring (L6)
pi_extensions: [ReceiptChainGuard]
inputs:
  - batch_report.json
  - execution_report.json
  - validation/verdicts/*.md
  - distribution/manifest.json
outputs:
  - Formatted CLI output
  - Optional: production_report.html (exportable)
depends_on: [story-7.2]
---

# ccf-report — Production Dashboard & Reporting

## Purpose
Read existing batch reports and display a formatted summary of production metrics, quality scores, token usage, and distribution outputs.

## Usage
```
ccf-report --project <path>
ccf-report --project <path> --format html
ccf-report --project <path> --blueprint <id>  (single blueprint detail)
```

## CLI Dashboard Format

```
+----------------------------------------------------+
|  CCF Production Report                             |
|  Project: Coach Adele / Batch-W07                  |
+----------------------------------------------------+

  BLUEPRINTS
  ----------
  Total:       12
  Authorized:  10  (83%)
  Remediated:   1  ( 8%)
  Escalated:    1  ( 8%)

  QUALITY SCORES
  --------------
  Avg Humanity:    8.2 / 10
  Avg Alchemy:     7.8 / 10
  Turing Pass:     100%
  Red Flags:       0
  Vulnerability:   10/10 scripts have 3-part move

  TOKEN USAGE
  -----------
  Total Input:     847,234 tokens
  Total Output:    124,891 tokens
  Estimated Cost:  $25.40

  TIMING
  ------
  Total Duration:      4h 23m
  Avg Per Blueprint:   21m 56s
  Fastest Blueprint:   14m 12s
  Slowest Blueprint:   38m 45s

  DISTRIBUTION
  ------------
  Tweets Generated:        30
  Captions Generated:      30
  Quote Cards Generated:   30
  Visual Prompts Generated: 10

  PER-BLUEPRINT DETAIL
  --------------------
  #  | Title                          | Result     | Humanity | Alchemy | Duration
  1  | Confident Investor Blueprint   | AUTHORIZED |  8.5     |  7.9    | 21m
  2  | Morning Routine Mastery        | AUTHORIZED |  8.8     |  8.2    | 18m
  3  | Debt Freedom Playbook          | REMEDIATED |  7.2     |  7.0    | 34m
  ...
  12 | Legacy Building Strategy       | ESCALATED  |  5.1     |  4.8    | 38m

+----------------------------------------------------+
```

## Data Sources
- `batch_report.json` from Story 7.2 (aggregate metrics)
- `execution_report.json` from Story 7.1 (per-blueprint details)
- `validation/verdicts/*.md` from Story 5.2 (validation decisions)
- `distribution/manifest.json` from Story 6.3 (output counts)
- `validation/analysis/*_analysis_report.json` from Story 5.1 (dimension scores)

## Report Modes

### Default: Summary
Shows the dashboard above with aggregate metrics.

### --blueprint <id>: Single Blueprint Detail
Shows detailed breakdown for one blueprint:
- All validation dimension scores
- Alchemy principle scores (10 individual)
- Vulnerability Move detection result
- Token usage breakdown by session
- Complete remediation history (if any)

### --format html: Export
Generates `production_report.html` — a portable report that can be shared with stakeholders.

## I-R-E-V-C Session Protocol

### INGEST
- Load batch_report.json, execution_report.json, validation verdicts, distribution manifest

### REASON
- Aggregate metrics across all blueprints
- Calculate averages, percentages, costs
- Rank blueprints by quality score

### EMIT
- Formatted CLI output (default)
- Optional: production_report.html

### VALIDATE
- All data sources present and parseable
- Metrics are internally consistent (totals match per-blueprint sums)
- No missing blueprints in report

### CHECKPOINT
- N/A (read-only reporting)
