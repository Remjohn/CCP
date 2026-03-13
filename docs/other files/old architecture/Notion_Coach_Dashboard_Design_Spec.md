# Notion Coach Dashboard Design Spec

## 20 Ways to Make the CCP Notion Workspace Feel Like Home

**Document Type:** Architecture Decision Record — Notion Delivery Layer Aesthetics & UX  
**Principle:** If it looks like AI generated it, it fails. If it feels like a tool, it fails. If it feels like *their* space — we win.

---

## The Problem With Default Notion Output

Every AI system that pushes content into Notion does the same thing: plain paragraph blocks, uniform structure, no visual rhythm. The coach opens the page and immediately feels like they're reading a machine's output. The goal of this spec is the opposite — when a coach opens their CCP workspace, it should feel like a space they designed themselves. Familiar. Warm. Structured but not clinical.

This document defines 20 design techniques — each mapped to a specific Notion feature and a specific CCP use case — that collectively transform the coach's workspace from "AI delivery endpoint" into "my command center."

---

## Part 1: Conditional Color — Visual Intelligence at a Glance

Notion's conditional color system allows background colors to be applied to database rows and gallery cards based on property rules. Unlike filters (which hide data), conditional color highlights data while keeping everything visible. It works across table, list, gallery, board, and timeline views.

### 1. 🔴 Overdue Content Alert

**Database:** Content Calendar  
**Rule:** Where `Publish Date` is before today → red background  
**Effect:** The coach opens their Content Calendar and overdue posts scream for attention without any filtering. Posts still due later stay clean. No mental parsing needed — red means act now.

### 2. 🟢 Client Engagement Heat Map

**Database:** Client Intelligence  
**Rule:** Where `Ritual Streak` is greater than or equal to 14 → green background  
**Effect:** Active, engaged clients glow green. The coach scans the database and instantly sees who is thriving. Combined with a second rule (where `Days Since Last Contact` is greater than 7 → red background), dormant clients surface automatically. Two rules, zero spreadsheet work.

### 3. 🟡 High-Priority Session Flagging

**Database:** Client Intelligence  
**Rule:** Where `Sentiment Trend` is "Declining" → yellow background  
**Effect:** Clients whose emotional arc is trending down get a warm visual nudge. The coach doesn't need to read every profile to decide who to call first — the color tells them.

### 4. 🟣 Status Match on Webinar Pipeline

**Database:** Webinar & Tierlist Assets  
**Rule:** Where `Status` is "Ready" → match option color (or custom purple background)  
**Effect:** In a board or gallery view, webinars that are complete and ready for delivery stand out from those still in drafting. The status color becomes the navigation.

### 5. 🟤 Photo Freshness Guard

**Database:** Personal Branding Photo Deck  
**Rule:** Where `Usage Count` is greater than or equal to 4 → brown/red background  
**Effect:** Overused photos are visually flagged. The coach knows which photos need refreshing without running any reports.

### 6. 🔵 Seasonal Content Alignment Check

**Database:** Content Calendar  
**Rule:** Where `Season` matches current month's archetype → blue background  
**Effect:** Posts that align to the active seasonal mandate get a cool blue glow. Off-season content stays neutral. The coach intuitively understands which content is "in season" without learning the 12-month rotation.

---

## Part 2: Layout Builder — Making Pages Feel Designed

Notion's Layout Builder allows database pages to have pinned property headers, a collapsible side property panel, and a clean content area. This transforms the default "endless scroll past properties" experience into something that feels like a designed application.

### 7. Pinned Properties as Content Identity Bar

**Database:** Content Calendar  
**Configuration:** Pin `Asset ID`, `Format`, `Platform`, and `Season` to the header row  
**Effect:** When the coach opens a content page, the four most important identity properties sit horizontally at the top — visible instantly, no scrolling. The rest of the properties (Publish Date, Status, trait scores) live in the collapsible side panel. The main page body stays clean for the script, visuals, and voice note.

### 8. Side Panel for Client Metadata

**Database:** Client Intelligence  
**Configuration:** Pin `Person ID` and `Status` to the header. Move all other properties (Ritual Streak, Sentiment, Onboarding Date, Phase) to the side panel.  
**Effect:** The client page body becomes a narrative space — psychological profile, voice journal, emotional arc — while the structured data lives neatly to the right. Toggle it open when needed, collapse it when reading. The page feels like a patient chart in a private practice, not a spreadsheet row.

---

## Part 3: Tabbed Layouts — One Page, Multiple Perspectives

Tabbed layouts attach database views directly to every page in a database as structural tabs. Unlike templates (which are blueprints that don't update), tabbed layouts are structural — change them once, every page in the database updates.

### 9. Content Page: Script + Visuals + Metrics Tabs

**Database:** Content Calendar  
**Tabs:** `Content` (default — script, voice note, WHY THIS POST), `Visual Assets` (linked gallery of all `VIMG` and `QUOT` assets tied to this content piece), `Performance` (engagement data once published)  
**Effect:** The coach writes or reviews the script in one tab. Switches to Visuals to see all images at once in a gallery. Switches to Performance after publishing to see how the post did. One page, three purposes, zero clutter.

### 10. Client Page: Profile + Sessions + Voice Journal Tabs

**Database:** Client Intelligence  
**Tabs:** `Profile` (default — psychological profile, emotional arc, patterns), `Sessions` (linked database view of all `SESS` entries sorted by date), `Voice Journal` (linked database view of all `VOIC` entries with audio embeds)  
**Effect:** The coach doesn't scroll through a single endless page. They flip between tabs depending on whether they're preparing for a session (Profile), reviewing past sessions (Sessions), or re-listening to a client's words (Voice Journal). Each tab is a different mode of interaction with the same client.

---

## Part 4: Automations — Making the Workspace Alive

Notion's automations feature now includes custom formulas in actions, define variables for multi-step logic, send notification, send email, and send webhook. The last one — webhooks — is the bridge between Notion and the CCP pipeline.

### 11. Status Change → Webhook to CCP Pipeline

**Trigger:** Coach changes content piece Status from "Draft" to "Approved"  
**Action:** Send webhook to `notion_sync.py` endpoint  
**Effect:** The coach's approval doesn't just change a label — it triggers the actual distribution pipeline. No separate "publish" button. No external app. The coach makes a decision in Notion and the system responds. This is the invisible bridge between Notion and the CCP backend.

### 12. New Client Onboarding → Auto-Assign Person ID

**Trigger:** New page created in Client Intelligence database  
**Action:** Use custom formula to read `coach_registry.json` next_client_id, format the Person ID (`CCC-NNNN`), write it to the Person ID property, increment the counter via webhook  
**Effect:** The coach adds a new client name. The Person ID appears automatically within seconds. No manual ID assignment, no registry lookup.

### 13. Publish Date Approaching → Coach Notification

**Trigger:** Content Calendar automation where `Publish Date` is tomorrow AND `Status` is still "Draft"  
**Action:** Send notification to coach: "You have unapproved content scheduled for tomorrow"  
**Effect:** A gentle nudge the day before — inside Notion's native notification system. Not an email from an unknown tool. Not a Telegram message from a bot. A Notion notification, from their own workspace.

---

## Part 5: Smart Formulas — Intelligence Without Dashboards

### 14. 🔴 Countdown Pulse (Days Until Publish)

**Formula:** Dynamic date math that shows `🔴 OVERDUE`, `🟠 TODAY`, `🟡 2d`, or `🟢 7d`  
**Effect:** Every content piece in the calendar has a single, color-coded urgency indicator. The coach scans the column and knows the state of their entire week without reading any dates.

### 15. 🟤 Client Progress Bar (Emoji-Based)

**Formula:** Converts milestone completion ratio into `🟤🟤🟤🟤🟤🟤⚪⚪⚪⚪` — a visual progress bar using colored and empty circles  
**Effect:** No charts. No external tools. A progress bar built entirely from emoji, rendered inline in the database. The coach sees 60% complete at a glance. This technique — using `slice()` on a string of repeated emoji — creates dashboard-quality visuals in a single formula property.

### 16. 🟢 Engagement Heat (Stacked Indicators)

**Formula:** Nested `if()` that converts `Ritual Streak` into `🟢🟢🟢 ON FIRE` / `🟢🟢 STRONG` / `🟢 BUILDING` / `🟡 STARTING` / `🔴 DORMANT`  
**Effect:** More expressive than a number. The text label gives emotional context — "ON FIRE" feels different from "21" even though they mean the same thing. For a coaching practice, emotional language is appropriate and expected.

### 17. 🟣 Content-to-Client Resonance Hit

**Formula:** Cross-references content theme tags against client top patterns using `includes()`. Returns `🟣 RESONANCE HIT` when a match is found.  
**Effect:** The coach sees that a post they're about to publish directly mirrors a pattern one of their clients is working through. They can share it personally: "I wrote something today that reminded me of what you said last week." The CCF and CBCS worlds bridge in a single formula column.

### 18. 🔵 Seasonal Indicator (Color-Emoji Formula)

**Formula:** Maps each monthly archetype to a color-based emoji: 🔵 The Architect, 🔴 The Warrior, 🟡 The Sun, 🖤 The Shadow, 🍊 The Garden, etc.  
**Effect:** Every content piece carries its seasonal identity without text clutter. The color emojis create a visual rhythm across the calendar — the coach sees orange clusters in June, red in April, blue in January. Seasonal identity becomes felt, not read.

---

## Part 6: Database Buttons — One-Click Actions

### 19. "Start Session" Button on Client Pages

**Button Action:** Creates a new `SESS` entry in the sessions database, auto-fills the client relation, sets the date to today, and opens the new session page in Side Peek  
**Effect:** One click, the session page is created and linked. No manual data entry. No navigating to a different database. The coach clicks → writes their session notes → done.

### 20. "Refresh Profile" Button on Client Pages

**Button Action:** Sends a webhook to the CBCS backend requesting a fresh Aria extraction for this client based on their latest voice messages  
**Effect:** The coach reads a client profile, feels it's outdated, clicks "Refresh Profile," and within minutes the psychological profile updates with new patterns from recent interactions. The button makes the invisible system accessible without exposing it.

---

## Part 7: Structural Polish — The Details That Build Trust

These aren't features. They're details. And details are what separate "a tool" from "my space."

### Technique 21: Floating Table of Contents

Every long-form client page (psychological profile, emotional arc, voice journal) gets heading blocks that power Notion's floating table of contents. The coach hovers over the left-side indicator and jumps to any section. No scrolling through 6 months of session summaries to find this week's entry.

### Technique 22: URL Mentions for External Links

When linking to Supabase-hosted audio files or external resources, use Notion's URL mention feature (paste → select mention) instead of raw URLs. Each link shows as a clean favicon + title inline mention, not a gobbledygook URL. The coach sees "🔗 Voice Note — March 1" instead of `https://xyz.supabase.co/storage/v1/object/public/...`.

### Technique 23: Custom Emoji for Asset Type Tags

Upload custom emoji for each content format: a specific icon for Storytelling, a different one for Case Study, another for Humor. These replace generic text labels in Select properties. When the coach scans the Content Calendar, format types are visually distinct — not just text in a colored pill, but a custom icon that feels branded.

### Technique 24: Pinned Tabs for Daily View

On the Notion desktop app, the coach pins 3 tabs: Content Calendar (this week's view), Client Intelligence (sorted by last interaction), and Photo Deck. These open automatically when Notion launches. Their workspace is ready before they are.

---

## Design Rule Summary

| Principle | Implementation |
|---|---|
| **No AI fingerprints** | Bold + colored backgrounds + color emoji for structure. No ✨, no "AI-looking" emoji. |
| **Color = meaning** | 🟢 good, 🟡 attention, 🔴 action, 🟣 insight, 🔵 info — consistent everywhere |
| **Structure, not decoration** | Every visual element serves navigation. Nothing is ornamental. |
| **Conditional color > filters** | Show everything, highlight what matters. Don't hide data. |
| **Tabs > scrolling** | Multiple perspectives on the same entity, not one endless page. |
| **Buttons > workflows** | One click in Notion replaces multi-step processes. |
| **The Sovereign Image Rule** | Real photos for the coach. AI images for client scenarios only. |
| **Never Outshine the Master** | Every deliverable traces to the coach's voice. The system is invisible. |

---

*This spec defines the aesthetic and UX layer of the CCP Notion Delivery Architecture. It complements §8.3 and §8.4 of the CCP Technical Architecture.*
