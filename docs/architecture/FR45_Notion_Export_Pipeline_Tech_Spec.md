# Tech-Spec: FR45 — Notion Export Pipeline (DEP-ENG-039)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Notion Delivery Layer (FR30-FR34)
**Skill Implementation:** `scripts/utils/notion_sync.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`

---

## 2. Overview

### Problem Statement
An AI system that forces a non-technical end-user (a high-ticket coach) to log into Supabase, read JSON files, or parse raw Markdown from a Git repository violates the core CCP mandate ("Never Outshine the Master"). If the cognitive load of retrieving the content is higher than the cognitive load of just writing the content manually, the coach will abandon the platform. The system generates massive underlying complexity (graphs, receipts, rationale), but the user must see none of it.

### Solution
FR45 defines the **Notion Export Pipeline (DEP-ENG-039)** via the `notion_sync.py` script. Upon completion of any compilation cycle (CCF Script, V²WS Webinar, or CBCS Client Summary), the Orchestrator invokes this Python tool to map the raw Supabase output directly to the coach's private Notion Workspace. It utilizes pre-defined UUID layouts to build tabbed, visually rich pages ensuring that deliverables are presented cleanly, natively, and securely.

### Scope
**In scope:**
- The `notion_sync.py` Python HTTP client executing API calls to Notion.
- The 7-section content page layout (Voice Note, "Why", Scripts, etc).
- Asset ID traceability insertion.
- The reverse-webhook listener supporting Notion Status `Approved` triggers.

**Out of scope:**
- Performance metric updates (handled by FR42 via Python CRON script).
- Notion Smart Formulas programming (these are UX features handled via Notion UI templates, not via API).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-039` | Notion Sync Script | OUTPUT — The `notion_sync.py` script acting as the delivery bridge. |
| Supabase `videos`/`scripts` | Compiled Assets | INPUT — The finalized data object waiting for delivery. |
| Supabase `coach_config` | Routing Keys | DEPENDENCY — Contains the specific Database IDs for the tenant's Notion workspace. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Cognitive Load Theory in Interface Design** | Sweller | 1988 | Establishes that intrinsic cognitive load is worsened by extraneous load (complex UI navigation). By moving all AI operations "under the hood" and surface deliverables in Notion—a tool most coaches already use—we effectively reduce the extraneous load of the CCP to zero. |

### Technical Decisions
1. **Python > Workflow Builders for Asset Sync:** While the CRON worker handles the scheduled Publer metrics (FR42), delivering the complex *content* of a compiled asset requires complex logic (e.g., mapping a V²WS `.excalidraw` JSON into a Notion File Block, and mapping paragraph breaks into Notion Text Blocks). The `notion_sync.py` script handles payload translation far more deterministically than a visual flow builder.
2. **Reverse Webhooks:** When the coach reviews a Draft in Notion and changes the target column to "Approved", the platform must know. Notion does not natively push webhooks. Therefore, an API integration polling worker (or Python webhook proxy) is required to watch for `Status` mutations.
3. **The Sovereign Image Rule:** The API is mathematically restricted from attaching AI-generated hero images to the Coach's face. If an image is required, `notion_sync.py` *must* query the coach's "Personal Branding Photo Deck" database first.

---

## 4. Implementation Plan

### Stage 1: Payload Construction & Routing
*Component:* `notion_sync.py` (Phase 1)
*Inputs:* Asset `[Universal_Asset_ID]`, `coach_id`.
*Outputs:* Formatted Notion API JSON Payload.
*Failure Condition:* Fails to retrieve `notion_workspace_id` from Supabase `coach_config`, orphanating the data.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Script receives execution flag from Orchestrator post-compilation.
2. Queries Supabase `coach_config` using `coach_id` to retrieve the Bearer Token and the target `notion_content_library_db` ID.
3. Queries Supabase `fingerprint_archive` and `scripts` using `Universal_Asset_ID` to retrieve the compiled assets.
4. If Asset requires a photo, trigger `get_sovereign_image()` querying the Notion Photo Deck DB for a mood-matching real photograph.

### Stage 2: Page Generation (The 7 Sections)
*Component:* `notion_sync.py` (Phase 2)
*Inputs:* Formatted Payload.
*Outputs:* HTTP POST to Notion API (`/v1/pages`).
*Failure Condition:* Notion API rejects the payload due to block limit size (>100 child blocks per request). Script fails to chunk the upload.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Construct the Notion Page object targeting exactly 7 layout sections:
   - **Coach Voice Note:** URL block linking to the raw audio (S3).
   - **Why This Post:** Callout block quoting the `Context_Selection_Rationale`.
   - **Leadership Farming:** Bulleted list mapping the character trait being developed.
   - **Script:** The primary text block (Markdown to Notion-Block parsed).
   - **Coach Photo:** Image block pulling from Sovereign Image query.
   - **Visual Assets:** File blocks linking to AI `.excalidraw` or `.webp` files.
   - **Posting Notes:** Instructions on hook pacing or comment replies.
2. Append the Universal Asset ID (`AAAA-CCC-MM-YY-XXXX`) into the Notion Page Properties.
3. POST the payload. 
4. Check response = 200 OK. Apply exponential backoff sequence if Rate Limited (HTTP 429).

### Stage 3: The Approval Webhook Listener
*Component:* `approval_watcher.py` (or Python proxy)
*Inputs:* Notion API Polling.
*Outputs:* Supabase `status` mutation.
*Failure Condition:* Poller fails to run, leaving an Approved asset stranded in Notion perpetually.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. A CRON script runs every 5 minutes querying the Notion Content DB for pages where `Status == 'Approved'` AND `Sync_Flag == False`.
2. Extract the Universal Asset ID from the page properties.
3. Emit a `REST` call to Supabase setting `videos.status = READY_TO_PUBLISH`.
4. Update Notion page property `Sync_Flag = True` to prevent endless double-polling.

---

## 5. Primary Output Schema (DEP-ENG-039)

**Schema Name:** `notion_page_creation_payload.json` (Fragment)

```json
{
  "parent": { "database_id": "notion_workspace_db_778899" },
  "properties": {
    "Title": { "title": [{"text": {"content": "The Burnout Myth"}}]},
    "Status": { "status": {"name": "Draft"}},
    "Universal_Asset_ID": { "rich_text": [{"text": {"content": "CCF_SCR-C01-03-26-8891"}}]},
    "Arc_Type": { "select": {"name": "Myth_Debunk"}}
  },
  "children": [
    {
      "object": "block",
      "type": "callout",
      "callout": {
        "rich_text": [{"text": {"content": "Why This Post: Based on the 03/12 voice note regarding client exhaustion. Mapped to Industry Mythology framework."}}],
        "icon": { "emoji": "💡" }
      }
    },
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": { "rich_text": [{"text": {"content": "The Script"}}] }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": { "rich_text": [{"text": {"content": "Most of the industry tells you to rest. They are wrong..."}}] }
    }
  ]
}
```

---

## 6. Backward Compatibility Fallback
If the Notion API experiences a severe outage or invalid token error (`HTTP 401`), the `notion_sync.py` script catches the exception and routes the compiled payload to emergency fallback storage (an S3 bucket holding raw `.md` equivalents). It immediately fires a Telegram message to the System Operator: `WARN: Notion Sync failed for Tenant X. Deliverables stranded in Fallback Bucket. API Token investigation required.` The compilation pipeline does not crash; the delivery is merely suspended.

---

## 7. Tasks

- [ ] **Task 1:** Write the `notion_sync.py` HTTP client initialization, configuring `Bearer` authentication dynamically based on `coach_id` lookups.
- [ ] **Task 2:** Write the Markdown-to-Notion block parser. Scripts generated by the agentic pipeline in `.md` (headers, bolding, bullet points) must be converted into strict Notion JSON Block objects.
- [ ] **Task 3:** Implement the Sovereign Image check. Write the API query that fetches `Category=Matching` from the "Personal Branding Photo Deck" database before rendering the page.
- [ ] **Task 4:** Write the `approval_watcher.py` CRON polling script to identify `Status == 'Approved'` mutations.
- [ ] **Task 5:** Write the 100-child-block chunking logic to prevent Notion API `payload too large` error rejections.

---

## 8. Acceptance Criteria

- [ ] **AC1 (The 7-Section Generation):** Manually trigger `notion_sync.py` passing a mocked Supabase compilation ID. Assert that the resulting Notion API response returns HTTP 200, and a manual inspection of the Notion workspace reveals all 7 required sections (Voice Note, Why, Leadership, Script, Photo, Visuals, Notes) perfectly formatted. *Failure Example:* The script dumps everything into a single unformatted paragraph block.
- [ ] **AC2 (Sovereign Image Enforcement):** Submit a script without attaching a primary image. Assert that `notion_sync.py` connects to the Photo Deck DB, extracts a legitimate Coach photograph URL, and injects it into the Payload. *Failure Example:* The system attaches an AI-generated Dall-E stick figure as the Coach's profile representation.
- [ ] **AC3 (Approval Trigger execution):** Log into Notion and change a Draft page's Status property to "Approved". Wait for the 5-minute polling window. Assert the Supabase database for that Asset ID flips to `READY_TO_PUBLISH`. *Failure Example:* The Coach approves the draft, but the system never pushes it to Publer because the poller failed to update Supabase.
- [ ] **AC4 (Rate Limit Backoff):** Mock a Notion API `HTTP 429 Too Many Requests` response. Assert that `notion_sync.py` sleeps for the header-requested timeout period, retries perfectly, and logs the delay. *Failure Example:* The script crashes, dropping the compiled asset entirely.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Notion API (`v1/pages`, `v1/blocks`) | External | The ultimate recipient of the intelligence output. |
| Supabase `coach_config` | Internal | The key-store containing the specific Database IDs required to route the document to the corresponding tab. |
| Universal Asset Registry | Internal | The centralized logging system ensuring `AAAA-CCC-MM-YY-XXXX` is correctly incremented and appended. |

---

## 10. Testing Strategy

### Unit Tests
- **Block Parsing Engine Check:** Pass a markdown string `## Header\n**Bold Text**\n- Bullet 1` to the parser. Assert it returns exactly 3 properly structured Notion objects (`heading_2`, `paragraph` with `annotations.bold: true`, and `bulleted_list_item`).

### Integration Tests
- **End-to-End Notion Sync Delivery:**
  1. Populate Supabase with 1 fully compiled script package (text, context, rationale, asset urls).
  2. Execute `notion_sync.py`.
  3. Validate the `HTTP 200` response from Notion.
  4. Query the Notion Page ID via API to assert the properties block correctly contains `Universal_Asset_ID`.

### Safety Tests (ADR-01 Quarantine Security)
- **Token Isolation Mismatch Validation:** Manipulate the script to attempt creating a page inside Coach A's Database ID using Coach B's API Token. Assert the Notion API throws exactly an `HTTP 404/403` error and the script cleanly logs the cross-tenant breach attempt without crashing the service.
