---
name: ccp-schedule
description: Schedule orchestration — configure the 7-stage CRON pipeline for coach content and client accountability
---

# /ccp-schedule {coach_acronym}

// turbo-all

> **Objective:** Configure the full CCP scheduling infrastructure via AWS EventBridge Scheduler. Orchestrates the two-clock system: (1) Weekly Coach Content Batch (Sunday 22:00) and (2) Program-Dependent Client Accountability (4+1+2 template).

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify EventBridge connectivity & .env", status: "pending" },
    { id: "step-2", description: "STEP 2: CONFIGURE-CONTENT-BATCH - Sunday 22:00 ccf-weekly trigger", status: "pending" },
    { id: "step-3", description: "STEP 3: CONFIGURE-COACH-RECORDING - Map weekly recording window", status: "pending" },
    { id: "step-4", description: "STEP 4: CONFIGURE-CLIENT-ACCOUNTABILITY - Set per-client CRON slots", status: "pending" },
    { id: "step-5", description: "STEP 5: CONFIGURE-CMF - Trigger CMF pipeline post-generation", status: "pending" },
    { id: "step-6", description: "STEP 6: VERIFY - Confirm all rules are active via AWS CLI", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update scheduled_monitor_config.json", status: "pending" }
  ]
});
```

**DO NOT PROCEED until you have called `write_todos` above.**

---

## STEP 1: PRE-FLIGHT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify EventBridge connectivity & .env", status: "in_progress" },
    { id: "step-2", description: "STEP-2: ...", status: "pending" },
    { id: "step-3", description: "STEP-3: ...", status: "pending" },
    { id: "step-4", description: "STEP-4: ...", status: "pending" },
    { id: "step-5", description: "STEP-5: ...", status: "pending" },
    { id: "step-6", description: "STEP-6: ...", status: "pending" },
    { id: "step-7", description: "STEP-7: ...", status: "pending" }
] });
```

| Check | Tool / Path | Expected |
|-------|-------------|----------|
| 1 | `aws sts get-caller-identity` | Valid IAM credentials with EventBridge access |
| 2 | `.env` | `GEMINI_API_KEY` and `TELEGRAM_BOT_TOKEN` present |
| 3 | `src/ccp/agents/scheduled_monitor.py` | File exists |
| 4 | `src/ccp/services/scheduled_monitor_service.py` | File exists |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify EventBridge connectivity & .env", status: "completed" },
    { id: "step-2", description: "STEP 2: CONFIGURE-CONTENT-BATCH - Sunday 22:00 ccf-weekly trigger", status: "pending" },
    { id: "step-3", description: "STEP-3: ...", status: "pending" },
    { id: "step-4", description: "STEP-4: ...", status: "pending" },
    { id: "step-5", description: "STEP-5: ...", status: "pending" },
    { id: "step-6", description: "STEP-6: ...", status: "pending" },
    { id: "step-7", description: "STEP-7: ...", status: "pending" }
] });
```

---

## STEP 2: CONFIGURE-CONTENT-BATCH

1. Create/Update EventBridge Schedule: `ccf-weekly-{coach_acronym}`
2. Expression: `cron(0 22 ? * SUN *)` # Sunday 22:00
3. Target: `lambda:run-ccf-batch` with payload `{"coach_acronym": "{coach_acronym}"}`

---

## STEP 4: CONFIGURE-CLIENT-ACCOUNTABILITY

1. Query `coaching_programs` table for the specific coach.
2. For each active program, extract `check_in_schedule`. 
3. Create individual EventBridge schedules for each client in the program.
4. Payload: `{"client_id": "...", "program_id": "...", "type": "proactive_journaling"}`

---

## STEP 6: VERIFY

**EXECUTE:**
```bash
aws scheduler list-schedules --region eu-west-1 --name-prefix ccp-{coach_acronym}
```

---

## STEP 7: CHECKPOINT

Update `config/scheduled_monitor_config.json`:
- `last_run = current_timestamp`
- `active = true`
- `run_count = run_count + 1`

**WHEN COMPLETE, EXECUTE:**
```javascript
write_todos({ todos: [
    { id: "step-1", description: "...", status: "completed" },
    { id: "step-2", description: "...", status: "completed" },
    { id: "step-3", description: "...", status: "completed" },
    { id: "step-4", description: "...", status: "completed" },
    { id: "step-5", description: "...", status: "completed" },
    { id: "step-6", description: "...", status: "completed" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update scheduled_monitor_config.json", status: "completed" }
] });
```
