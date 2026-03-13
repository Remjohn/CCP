"""
CMF Automator Generator V3 (with Motion Phase + Validation)
Generates `RUN_PIPELINE.ps1` and `COMMANDS.md` scripts for Gemini CLI execution.

Model Strategy:
- gemini-3-pro-preview:   High EQ tasks (Diagnose, Compose, Storyboard, Motion)
- gemini-3-flash-preview: High volume/speed tasks (Hunt, Analyze, Script, Authorize, Assets)

CLI: gemini -p "prompt" --yolo --model <model>
"""

import os
import argparse
from pathlib import Path

BASE_PATH = r"d:\Work\The Conscious Movie Factory December"

# =============================================================================
# RUN_PIPELINE.ps1 TEMPLATE (V3 with Motion Phase + GMG Validation)
# =============================================================================

PIPELINE_TEMPLATE = '''<#
    CMF GEMINI CLI PIPELINE - {project_id}
    ==========================================
    Pure Gemini CLI Execution with RESUMABILITY
    
    Model Strategy:
    - gemini-3-pro-preview:   High EQ tasks (Diagnosis, Compose, Storyboard, Motion)
    - gemini-3-flash-preview: High volume/speed tasks (Hunt, Analyze, Script, Auth)
    
    CLI: gemini -p "prompt" --yolo --model <model>
    
    RESUME SUPPORT:
    - Tracks completed steps in .pipeline_checkpoint file
    - Use -Resume to skip already-completed steps
    - Use -StartFrom "step-name" to start from a specific step
    - Use -Reset to clear checkpoint and start fresh
#>

param(
    [string]$Command = "",
    [ValidateSet("1a", "1b", "motion", "assets", "all", "")]
    [string]$Phase = "",
    [switch]$Resume,          # Skip completed steps
    [string]$StartFrom = "",  # Start from specific step (e.g. "cmf-compose")
    [switch]$Reset,           # Clear checkpoint file and start fresh
    [switch]$Status           # Show current checkpoint status
)

$ErrorActionPreference = "Stop"
$projectPath = $PSScriptRoot
$projectId = "{project_id}"
$basePath = "{base_path}"

# Checkpoint file for tracking completed steps
$checkpointFile = Join-Path $projectPath ".pipeline_checkpoint"

# --- 1. CONFIGURATION & SETUP ---

# Load .env variables (for API keys if needed)
$envFile = Join-Path $basePath ".env"
if (Test-Path $envFile) {{
    Get-Content $envFile | ForEach-Object {{
        if ($_ -match "^([^#][^=]*)=(.*)$") {{
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim())
        }}
    }}
}}

# --- 1b. LOGGING SETUP ---
$logDir = Join-Path $basePath ".logs"
if (-not (Test-Path $logDir)) {{ New-Item -ItemType Directory -Force -Path $logDir | Out-Null }}
$logFile = Join-Path $logDir "${{projectId}}_pipeline.log"

# --- 2. CHECKPOINT FUNCTIONS ---

function Get-CompletedSteps {{
    if (Test-Path $checkpointFile) {{
        return @(Get-Content $checkpointFile | Where-Object {{ $_ -match '\\S' }})
    }}
    return @()
}}

function Add-CompletedStep {{
    param([string]$StepName)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$StepName|$timestamp" | Add-Content $checkpointFile
    Write-Host "  [CHECKPOINT] Saved: $StepName" -ForegroundColor DarkGreen
}}

function Is-StepCompleted {{
    param([string]$StepName)
    $completed = Get-CompletedSteps
    return ($completed | Where-Object {{ $_.StartsWith("$StepName|") }}).Count -gt 0
}}

function Reset-Checkpoint {{
    if (Test-Path $checkpointFile) {{
        Remove-Item $checkpointFile -Force
        Write-Host "  [RESET] Checkpoint cleared. Pipeline will start fresh." -ForegroundColor Yellow
    }} else {{
        Write-Host "  [RESET] No checkpoint file found." -ForegroundColor Gray
    }}
}}

function Show-CheckpointStatus {{
    Write-Host ""
    Write-Host "=== PIPELINE CHECKPOINT STATUS ===" -ForegroundColor Cyan
    Write-Host "Project: $projectId" -ForegroundColor Yellow
    Write-Host ""
    
    if (Test-Path $checkpointFile) {{
        $steps = Get-CompletedSteps
        if ($steps.Count -gt 0) {{
            Write-Host "Completed Steps:" -ForegroundColor Green
            foreach ($step in $steps) {{
                $parts = $step -split '\\|'
                Write-Host "  [OK] $($parts[0]) - $($parts[1])" -ForegroundColor Green
            }}
        }} else {{
            Write-Host "No steps completed yet." -ForegroundColor Gray
        }}
    }} else {{
        Write-Host "No checkpoint file. Pipeline not started or was reset." -ForegroundColor Gray
    }}
    Write-Host ""
}}

# Track if we've passed the StartFrom step
$script:startFromReached = ($StartFrom -eq "")

# --- 3. EXECUTION ENGINE ---

function Run-Gemini {{
    param(
        [string]$CommandFileBase,  # e.g. "cmf-diagnose"
        [string]$StepName,
        [ValidateSet("gemini-3-pro-preview", "gemini-3-flash-preview")]
        [string]$UseModel = "gemini-3-pro-preview"
    )

    # Check if we should skip (StartFrom logic)
    if (-not $script:startFromReached) {{
        if ($CommandFileBase -eq $StartFrom) {{
            $script:startFromReached = $true
            Write-Host "  [START FROM] Beginning from: $CommandFileBase" -ForegroundColor Cyan
        }} else {{
            Write-Host "  [SKIP] $CommandFileBase (waiting for $StartFrom)" -ForegroundColor DarkGray
            return
        }}
    }}

    # Check if already completed (Resume logic)
    if ($Resume -and (Is-StepCompleted $CommandFileBase)) {{
        Write-Host "  [SKIP] $CommandFileBase - Already completed (use -Reset to clear)" -ForegroundColor DarkYellow
        return
    }}

    Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan
    Write-Host "  STEP:  $StepName" -ForegroundColor Cyan
    Write-Host "  FILE:  $CommandFileBase.md" -ForegroundColor Gray
    Write-Host "  MODEL: $UseModel" -ForegroundColor Yellow
    Write-Host "  SESSION: FRESH (isolated)" -ForegroundColor Green
    Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan

    # Command files are in commands/ folder
    $cmdPath = Join-Path $basePath "commands\\$CommandFileBase.md"
    
    if (-not (Test-Path $cmdPath)) {{
        Write-Error "Command file not found: commands\\$CommandFileBase.md"
        exit 1
    }}
    
    # Read the command template
    $cmdTemplate = Get-Content $cmdPath -Raw
    
    # Prepare the prompt with project context
    $finalPrompt = @"
$cmdTemplate

EXECUTING FOR PROJECT ID: $projectId
PROJECT PATH: $projectPath
"@
    
    # Write prompt to temp file to avoid escaping issues
    $tempPromptFile = Join-Path $env:TEMP "cmf_prompt_$([guid]::NewGuid().ToString('N').Substring(0,8)).txt"
    $finalPrompt | Out-File -FilePath $tempPromptFile -Encoding UTF8
    
    # Set working directory for gemini
    Set-Location $basePath
    
    try {{
        # CRITICAL: Each command runs as a SEPARATE gemini process for session isolation
        Write-Host "  Launching fresh gemini session..." -ForegroundColor DarkGray
        
        $process = Start-Process -FilePath "cmd.exe" `
            -ArgumentList "/c type `"$tempPromptFile`" | gemini --yolo --model $UseModel" `
            -WorkingDirectory $basePath `
            -NoNewWindow `
            -Wait `
            -PassThru
        
        if ($process.ExitCode -ne 0) {{
            throw "Gemini CLI returned exit code $($process.ExitCode)"
        }}
        
        # Mark step as completed
        Add-CompletedStep $CommandFileBase
        
        Write-Host "  [OK] Session completed and terminated cleanly" -ForegroundColor Green
        
        # Brief pause between commands to avoid rate limiting
        Start-Sleep -Seconds 2
    }}
    catch {{
        Write-Host ""
        Write-Host "  [FAIL] STEP FAILED: $CommandFileBase" -ForegroundColor Red
        Write-Host "  To resume from this step, run:" -ForegroundColor Yellow
        Write-Host "    .\\RUN_PIPELINE.ps1 -Phase $Phase -Resume" -ForegroundColor White
        Write-Host "  Or to start exactly from this step:" -ForegroundColor Yellow
        Write-Host "    .\\RUN_PIPELINE.ps1 -Phase $Phase -StartFrom $CommandFileBase" -ForegroundColor White
        Write-Host ""
        throw $_
    }}
    finally {{
        # Cleanup temp file
        if (Test-Path $tempPromptFile) {{
            Remove-Item $tempPromptFile -Force
        }}
    }}
}}

# Run workflow files from commands/ folder (for motion phase)
function Run-Workflow {{
    param(
        [string]$WorkflowName,  # e.g. "cmf-compose-sb"
        [string]$StepName
    )

    # Check if we should skip (StartFrom logic)
    if (-not $script:startFromReached) {{
        if ($WorkflowName -eq $StartFrom) {{
            $script:startFromReached = $true
            Write-Host "  [START FROM] Beginning from: $WorkflowName" -ForegroundColor Cyan
        }} else {{
            Write-Host "  [SKIP] $WorkflowName (waiting for $StartFrom)" -ForegroundColor DarkGray
            return
        }}
    }}

    # Check if already completed (Resume logic)
    if ($Resume -and (Is-StepCompleted $WorkflowName)) {{
        Write-Host "  [SKIP] $WorkflowName - Already completed" -ForegroundColor DarkYellow
        return
    }}

    Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan
    Write-Host "  STEP:     $StepName" -ForegroundColor Cyan
    Write-Host "  WORKFLOW: /$WorkflowName" -ForegroundColor Gray
    Write-Host "  SESSION:  FRESH (isolated)" -ForegroundColor Green
    Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan

    $workflowPath = Join-Path $basePath "commands\\$WorkflowName.md"
    
    if (-not (Test-Path $workflowPath)) {{
        Write-Error "Command file not found: commands\\$WorkflowName.md"
        exit 1
    }}
    
    $workflowContent = Get-Content $workflowPath -Raw
    
    $finalPrompt = @"
$workflowContent

EXECUTING FOR PROJECT ID: $projectId
PROJECT PATH: $projectPath
"@
    
    $tempPromptFile = Join-Path $env:TEMP "cmf_workflow_$([guid]::NewGuid().ToString('N').Substring(0,8)).txt"
    $finalPrompt | Out-File -FilePath $tempPromptFile -Encoding UTF8
    
    Set-Location $basePath
    
    try {{
        Write-Host "  Launching fresh gemini session..." -ForegroundColor DarkGray
        
        $process = Start-Process -FilePath "cmd.exe" `
            -ArgumentList "/c type `"$tempPromptFile`" | gemini --yolo --model gemini-3-pro-preview" `
            -WorkingDirectory $basePath `
            -NoNewWindow `
            -Wait `
            -PassThru
        
        if ($process.ExitCode -ne 0) {{
            throw "Gemini CLI returned exit code $($process.ExitCode)"
        }}
        
        Add-CompletedStep $WorkflowName
        Write-Host "  [OK] Session completed" -ForegroundColor Green
        
        Start-Sleep -Seconds 2
    }}
    catch {{
        Write-Host ""
        Write-Host "  [FAIL] STEP FAILED: $WorkflowName" -ForegroundColor Red
        Write-Host "  To resume, run:" -ForegroundColor Yellow
        Write-Host "    .\\RUN_PIPELINE.ps1 -Phase motion -Resume" -ForegroundColor White
        throw $_
    }}
    finally {{
        if (Test-Path $tempPromptFile) {{
            Remove-Item $tempPromptFile -Force
        }}
    }}
}}

function Show-Banner {{
    Write-Host ""
    Write-Host "==================================================================" -ForegroundColor Magenta
    Write-Host " CMF GEMINI CLI PIPELINE (with Resume Support)                    " -ForegroundColor Magenta
    Write-Host "==================================================================" -ForegroundColor Magenta
    Write-Host "  Project: $projectId" -ForegroundColor Yellow
    Write-Host "  Models:  gemini-3-pro-preview (EQ), gemini-3-flash-preview (Speed)" -ForegroundColor Gray
    if ($Resume) {{
        Write-Host "  Mode:    RESUME (skipping completed steps)" -ForegroundColor Green
    }}
    if ($StartFrom) {{
        Write-Host "  Starting From: $StartFrom" -ForegroundColor Cyan
    }}
    Write-Host "==================================================================" -ForegroundColor Magenta
    Write-Host ""
}}

# --- 4. HANDLE SPECIAL FLAGS ---

if ($Reset) {{
    Reset-Checkpoint
    exit 0
}}

if ($Status) {{
    Show-CheckpointStatus
    exit 0
}}

# --- 5. PIPELINE DEFINITIONS ---

Start-Transcript -Path $logFile -Append
Show-Banner

if ($Command -ne "") {{
    Write-Warning "Custom command execution is deprecated. Use -Phase argument."
}}
elseif ($Phase -eq "1a") {{
    Write-Host "Running Phase 1A: Narrative..." -ForegroundColor Green
    
    Run-Gemini -CommandFileBase "cmf-diagnose" -StepName "Diagnosis (Pro)" -UseModel "gemini-3-pro-preview"
    
    # Generate Brand Avatar (requires avatar image in project folder)
    Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan
    Write-Host "  STEP:  Generate Brand Avatar" -ForegroundColor Cyan
    Write-Host "  TOOL:  generate_brand_avatar.py (OpenRouter + Qwen VL)" -ForegroundColor Gray
    Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan
    
    if (-not ($Resume -and (Is-StepCompleted "brand-avatar"))) {{
        try {{
            Set-Location $basePath
            python tools/generate_brand_avatar.py --project $projectId
            if ($LASTEXITCODE -eq 0) {{
                Add-CompletedStep "brand-avatar"
                Write-Host "  [OK] Brand Avatar created" -ForegroundColor Green
            }} else {{
                Write-Host "  [WARN] Brand Avatar generation failed (no avatar image?)" -ForegroundColor Yellow
                Write-Host "         Add *avatar*.png or *avatar*.jpg to project folder" -ForegroundColor Yellow
            }}
        }}
        catch {{
            Write-Host "  [WARN] Brand Avatar generation failed: $_" -ForegroundColor Yellow
        }}
    }} else {{
        Write-Host "  [SKIP] brand-avatar - Already completed" -ForegroundColor DarkYellow
    }}
    
    Run-Gemini -CommandFileBase "cmf-hunt" -StepName "Hunter (Pro)" -UseModel "gemini-3-pro-preview"
    Run-Gemini -CommandFileBase "cmf-analyze" -StepName "Analyst (Pro)" -UseModel "gemini-3-pro-preview"
    Run-Gemini -CommandFileBase "cmf-compose" -StepName "Composer (Pro)" -UseModel "gemini-3-pro-preview"
    Run-Gemini -CommandFileBase "cmf-authorize" -StepName "Authorization (Pro)" -UseModel "gemini-3-pro-preview"
    Run-Gemini -CommandFileBase "cmf-script" -StepName "Script Assembly (Pro)" -UseModel "gemini-3-pro-preview"
    Run-Gemini -CommandFileBase "cmf-beat-cluster" -StepName "Beat Cluster (Pro)" -UseModel "gemini-3-pro-preview"
}}
elseif ($Phase -eq "1b") {{
    Write-Host "Running Phase 1B: Pre-Motion (E-Roll -> Assets -> Sonic -> Visual Auth)..." -ForegroundColor Green
    Write-Host ""
    Write-Host "[INFO] Phase 1B prepares prerequisites. Run '-Phase motion' after 1B for visual prompts." -ForegroundColor Cyan
    Write-Host ""
    
    # CRITICAL: E-Roll must run FIRST (before Visual Schema)
    Write-Host 'STEP 1: E-Roll Research (REQUIRED before Visual Schema)' -ForegroundColor Yellow
    Run-Gemini -CommandFileBase "cmf-eroll" -StepName "E-Roll Research (Pro)" -UseModel "gemini-3-pro-preview"
    
    # Asset Procurement (uses Deep Research Report as input)
    Write-Host "STEP 2: Asset Procurement" -ForegroundColor Yellow
    Run-Gemini -CommandFileBase "cmf-assets" -StepName "Asset Procurement (Pro)" -UseModel "gemini-3-pro-preview"
    
    # Sonic prepares audio context
    Write-Host "STEP 3: Sonic Script" -ForegroundColor Yellow
    Run-Gemini -CommandFileBase "cmf-sonic" -StepName "Sonic (Pro)" -UseModel "gemini-3-pro-preview"
    
    # Visual Auth validates schema without generating prompts
    Write-Host "STEP 4: Visual Auth (Schema Validation)" -ForegroundColor Yellow
    Run-Gemini -CommandFileBase "cmf-visual-auth" -StepName "Visual Auth (Pro)" -UseModel "gemini-3-pro-preview"
    
    Write-Host ""
    Write-Host "[PHASE 1B COMPLETE] Prerequisites ready." -ForegroundColor Green
    Write-Host ""
    Write-Host ">>> NEXT: Run '-Phase motion' to generate visual prompts (SB + CAC + 6 GMG Experts) <<<" -ForegroundColor Yellow
    Write-Host ""
}}
elseif ($Phase -eq "assets") {{
    Write-Host "Running Asset Procurement (Additional E-Roll and Image Hunt)..." -ForegroundColor Green
    Write-Host "Note: E-Roll is now run automatically in Phase 1B" -ForegroundColor Yellow
    
    # Only run E-Roll if not already completed
    Run-Gemini -CommandFileBase "cmf-eroll" -StepName "E-Roll Research (Pro)" -UseModel "gemini-3-pro-preview"
    Run-Gemini -CommandFileBase "cmf-assets" -StepName "Asset Hunter (Flash)" -UseModel "gemini-3-flash-preview"
}}
elseif ($Phase -eq "motion") {{
    Write-Host "Running Motion V2: VCP-Driven Visual Pipeline..." -ForegroundColor Green
    Write-Host "  8 isolated sessions: SB + CAC + 6 GMG Experts" -ForegroundColor Yellow
    Write-Host "  NOTE: Compose commands now read directly from beat_cluster.json" -ForegroundColor Cyan
    Write-Host ""
    
    # --- STORYBOARD (Reaction Shots) ---
    Write-Host ">>> STORYBOARD (Reaction Shots) <<<" -ForegroundColor Yellow
    Run-Workflow -WorkflowName "cmf-compose-sb" -StepName "Compose SB Prompts (VCP)"
    
    # --- CAC (Conscious Ambient Cinema) ---
    Write-Host "`n>>> CAC (Vogue Living B-Roll) <<<" -ForegroundColor Yellow
    Run-Workflow -WorkflowName "cmf-compose-cac" -StepName "Compose CAC Prompts (VCP)"
    
    # --- GMG Expert 01: Neo-Schematic Architect ---
    Write-Host "`n>>> GMG Expert 01 (Systems/Networks) <<<" -ForegroundColor Yellow
    Run-Workflow -WorkflowName "cmf-compose-gmg-01" -StepName "Compose GMG-01 Prompts (VCP)"
    
    # VALIDATION: GMG01 must produce SC03 and SC04 files
    $gmgFolder = Join-Path $projectPath "prompts\\GMG"
    $gmg01Files = @("GMG01_SC03_T2I.txt", "GMG01_SC04_T2I.txt")
    $missingFiles = $gmg01Files | Where-Object {{ -not (Test-Path (Join-Path $gmgFolder $_)) }}
    if ($missingFiles.Count -gt 0) {{
        Write-Host "  [WARN] GMG01 validation failed: Missing $($missingFiles -join ', ')" -ForegroundColor Yellow
        Write-Host "  [RETRY] Clearing checkpoint and re-running GMG01..." -ForegroundColor Cyan
        # Remove GMG01 from checkpoint to allow retry
        $checkpointContent = Get-Content $checkpointFile | Where-Object {{ -not $_.StartsWith("cmf-compose-gmg-01|") }}
        $checkpointContent | Set-Content $checkpointFile
        Run-Workflow -WorkflowName "cmf-compose-gmg-01" -StepName "Compose GMG-01 Prompts (VCP) [RETRY]"
    }}
    
    # --- GMG Expert 02: Mono-Kinetic Protagonist ---
    Write-Host "`n>>> GMG Expert 02 (Silhouette/Weather) <<<" -ForegroundColor Yellow
    Run-Workflow -WorkflowName "cmf-compose-gmg-02" -StepName "Compose GMG-02 Prompts (VCP)"
    
    # --- GMG Expert 03: Emotional Animator ---
    Write-Host "`n>>> GMG Expert 03 (Emotions/Stick Figures) <<<" -ForegroundColor Yellow
    Run-Workflow -WorkflowName "cmf-compose-gmg-03" -StepName "Compose GMG-03 Prompts (VCP)"
    
    # --- GMG Expert 04: Paper Architect ---
    Write-Host "`n>>> GMG Expert 04 (Paper/Documents) <<<" -ForegroundColor Yellow
    Run-Workflow -WorkflowName "cmf-compose-gmg-04" -StepName "Compose GMG-04 Prompts (VCP)"
    
    # --- GMG Expert 05: Data Weaver ---
    Write-Host "`n>>> GMG Expert 05 (Product Reveals) <<<" -ForegroundColor Yellow
    Run-Workflow -WorkflowName "cmf-compose-gmg-05" -StepName "Compose GMG-05 Prompts (VCP)"
    
    # --- GMG Expert 06: Visual Synthesizer (NO GOLD) ---
    Write-Host "`n>>> GMG Expert 06 (Pure Geometry - NO GOLD) <<<" -ForegroundColor Yellow
    Run-Workflow -WorkflowName "cmf-compose-gmg-06" -StepName "Compose GMG-06 Prompts (VCP)"
    
    Write-Host ""
    Write-Host "[MOTION V2] All visual prompts generated (VCP-driven)." -ForegroundColor Green
    Write-Host "  Output folder: prompts/ in $projectPath" -ForegroundColor Cyan
}}
elseif ($Phase -eq "all") {{
    & $PSCommandPath -Phase "1a" -Resume:$Resume -StartFrom $StartFrom
    & $PSCommandPath -Phase "1b" -Resume:$Resume
    & $PSCommandPath -Phase "motion" -Resume:$Resume
}}
else {{
    Write-Host 'Usage: .\\RUN_PIPELINE.ps1 -Phase <1a|1b|motion|assets|all> [-Resume] [-StartFrom <step>] [-Reset] [-Status]' -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Phases:" -ForegroundColor Cyan
    Write-Host '  1a     - Narrative (Diagnose > Hunt > Analyze > Compose > Authorize > Script > Beat Cluster)'
    Write-Host '  1b     - Pre-Motion (E-Roll > Assets > Sonic > Visual Auth)'
    Write-Host '  motion - Motion V2: Visual prompts (SB + CAC + 6 GMG Experts) with SC naming'
    Write-Host "  assets - Additional E-Roll and Asset Procurement (optional)"
    Write-Host "  all    - Run 1a + 1b + motion sequentially"
    Write-Host ""
    Write-Host "Resume Options:" -ForegroundColor Cyan
    Write-Host "  -Resume              Skip steps that already completed successfully"
    Write-Host '  -StartFrom <step>    Start from a specific step (e.g. -StartFrom cmf-compose)'
    Write-Host "  -Reset               Clear checkpoint file and start fresh"
    Write-Host "  -Status              Show which steps have been completed"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Green
    Write-Host "  .\\RUN_PIPELINE.ps1 -Phase all                         # Run everything"
    Write-Host "  .\\RUN_PIPELINE.ps1 -Phase motion                      # Run motion V2 only"
    Write-Host "  .\\RUN_PIPELINE.ps1 -Phase motion -Resume              # Resume motion phase"
    Write-Host "  .\\RUN_PIPELINE.ps1 -Phase motion -StartFrom cmf-compose-gmg-03  # Start from GMG-03"
    Write-Host "  .\\RUN_PIPELINE.ps1 -Status                            # Check progress"
    Write-Host "  .\\RUN_PIPELINE.ps1 -Reset                             # Clear and restart"
}}

Stop-Transcript
Write-Host "`n[DONE] Pipeline Complete." -ForegroundColor Green
'''

# =============================================================================
# COMMANDS.md TEMPLATE (V2 with Motion Phase)
# =============================================================================

COMMANDS_TEMPLATE = '''# {project_id} - Pipeline Commands

## Quick Start (Full Pipeline)
```powershell
cd "{project_path}"
.\\RUN_PIPELINE.ps1 -Phase all
```

## Resume After Failure
```powershell
.\\RUN_PIPELINE.ps1 -Phase all -Resume
```

## Check Progress
```powershell
.\\RUN_PIPELINE.ps1 -Status
```

## Reset & Start Fresh
```powershell
.\\RUN_PIPELINE.ps1 -Reset
.\\RUN_PIPELINE.ps1 -Phase all
```

---

## Phase-by-Phase Execution

### Phase 1A: Narrative
```powershell
.\\RUN_PIPELINE.ps1 -Phase 1a
```

### Phase 1B: Visuals
```powershell
.\\RUN_PIPELINE.ps1 -Phase 1b
```

### Motion: VCP-Driven Visual Pipeline
```powershell
.\\RUN_PIPELINE.ps1 -Phase motion
```

### Assets: E-Roll & Procurement
```powershell
.\\RUN_PIPELINE.ps1 -Phase assets
```

---

## Start From Specific Step

### Phase 1A Steps
```powershell
.\\RUN_PIPELINE.ps1 -Phase 1a -StartFrom cmf-diagnose
.\\RUN_PIPELINE.ps1 -Phase 1a -StartFrom cmf-hunt
.\\RUN_PIPELINE.ps1 -Phase 1a -StartFrom cmf-analyze
.\\RUN_PIPELINE.ps1 -Phase 1a -StartFrom cmf-compose
.\\RUN_PIPELINE.ps1 -Phase 1a -StartFrom cmf-authorize
.\\RUN_PIPELINE.ps1 -Phase 1a -StartFrom cmf-script
.\\RUN_PIPELINE.ps1 -Phase 1a -StartFrom cmf-beat-cluster
```

### Phase 1B Steps
```powershell
.\\RUN_PIPELINE.ps1 -Phase 1b -StartFrom cmf-eroll
.\\RUN_PIPELINE.ps1 -Phase 1b -StartFrom cmf-assets
.\\RUN_PIPELINE.ps1 -Phase 1b -StartFrom cmf-storyboard
.\\RUN_PIPELINE.ps1 -Phase 1b -StartFrom cmf-sonic
.\\RUN_PIPELINE.ps1 -Phase 1b -StartFrom cmf-motion
.\\RUN_PIPELINE.ps1 -Phase 1b -StartFrom cmf-visual-auth
```

### Motion Steps
```powershell
.\\RUN_PIPELINE.ps1 -Phase motion -StartFrom cmf-compose-sb
.\\RUN_PIPELINE.ps1 -Phase motion -StartFrom cmf-compose-cac
.\\RUN_PIPELINE.ps1 -Phase motion -StartFrom cmf-compose-gmg-01
.\\RUN_PIPELINE.ps1 -Phase motion -StartFrom cmf-compose-gmg-02
.\\RUN_PIPELINE.ps1 -Phase motion -StartFrom cmf-compose-gmg-03
.\\RUN_PIPELINE.ps1 -Phase motion -StartFrom cmf-compose-gmg-04
.\\RUN_PIPELINE.ps1 -Phase motion -StartFrom cmf-compose-gmg-05
.\\RUN_PIPELINE.ps1 -Phase motion -StartFrom cmf-compose-gmg-06
```

### Asset Steps
```powershell
.\\RUN_PIPELINE.ps1 -Phase assets -StartFrom cmf-eroll
.\\RUN_PIPELINE.ps1 -Phase assets -StartFrom cmf-assets
```

---

## Generate RunningHub JSON
```powershell
cd "{base_path}"
python tools/populate_runninghub_v2.py --project "{project_id}"
```

Output: `{project_id} SCENES PROMPTS.json`

---

## Individual Gemini Commands (Manual Execution)

```powershell
cd "{base_path}"

# Phase 1A
gemini -p "Read commands/cmf-diagnose.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-hunt.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-analyze.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-compose.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-authorize.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-script.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-beat-cluster.md and execute for project {project_id}" --yolo

# Phase 1B
gemini -p "Read commands/cmf-eroll.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-assets.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-storyboard.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-sonic.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-motion.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-visual-auth.md and execute for project {project_id}" --yolo

# Motion Phase (VCP-Driven)
gemini -p "Read commands/cmf-compose-sb.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-compose-cac.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-compose-gmg-01.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-compose-gmg-02.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-compose-gmg-03.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-compose-gmg-04.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-compose-gmg-05.md and execute for project {project_id}" --yolo
gemini -p "Read commands/cmf-compose-gmg-06.md and execute for project {project_id}" --yolo
```
'''


# =============================================================================
# GENERATOR FUNCTIONS
# =============================================================================

def generate_pipeline(project_id: str, project_dir: Path) -> None:
    """Generate a RUN_PIPELINE.ps1 file for a project."""
    output_path = project_dir / "RUN_PIPELINE.ps1"
    content = PIPELINE_TEMPLATE.format(
        project_id=project_id,
        base_path=BASE_PATH
    )
    output_path.write_text(content, encoding='utf-8')
    print(f"  [OK] RUN_PIPELINE.ps1")


def generate_commands(project_id: str, project_dir: Path) -> None:
    """Generate a COMMANDS.md file for a project."""
    output_path = project_dir / "COMMANDS.md"
    content = COMMANDS_TEMPLATE.format(
        project_id=project_id,
        project_path=str(project_dir),
        base_path=BASE_PATH
    )
    output_path.write_text(content, encoding='utf-8')
    print(f"  [OK] COMMANDS.md")


def generate_script(project_id: str, coach: str = "Coach Adele") -> None:
    """
    Generate both RUN_PIPELINE.ps1 and COMMANDS.md for a project.
    Called by create_project.py
    """
    project_dir = Path(BASE_PATH) / "production" / coach / project_id
    
    if not project_dir.exists():
        print(f"[ERROR] Project directory not found: {project_dir}")
        return
    
    print(f"Generating automation files for: {project_id}")
    generate_pipeline(project_id, project_dir)
    generate_commands(project_id, project_dir)
    print(f"[DONE] Automation files created in {project_dir}")


def main():
    parser = argparse.ArgumentParser(description='Generate CMF Pipeline Scripts V3')
    parser.add_argument('--project', type=str, help='Specific project folder to generate for')
    parser.add_argument('--coach', type=str, default="Coach Adele", help='Coach folder name')
    parser.add_argument('--all', action='store_true', help='Generate for all known projects')
    args = parser.parse_args()
    
    # Known projects (can be expanded)
    projects = [
        "01_50-12 Matthis",
        "02_50-12 Audrey",
        "03_50-12 Jean Pierre",
        "04_50-12 Nina",
        "05_50-12 Fitou",
        "06_50-12 Monia"
    ]
    
    if args.all:
        print("Generating automation files for all projects...")
        for proj in projects:
            project_dir = Path(BASE_PATH) / "production" / args.coach / proj
            if project_dir.exists():
                print(f"\n{proj}:")
                generate_pipeline(proj, project_dir)
                generate_commands(proj, project_dir)
            else:
                print(f"\n{proj}: [SKIP] Directory not found")
        print("\n[DONE] All projects processed.")
    elif args.project:
        generate_script(args.project, args.coach)
    else:
        print("Usage:")
        print("  python generate_automator.py --all")
        print("  python generate_automator.py --project '02_50-12 Audrey'")
        print("  python generate_automator.py --project '02_50-12 Audrey' --coach 'Coach Sarah'")


if __name__ == "__main__":
    main()
