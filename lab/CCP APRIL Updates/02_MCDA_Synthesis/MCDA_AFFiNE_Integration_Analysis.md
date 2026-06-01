# Multi-Criteria Decision Analysis (MCDA): AFFiNE as the Branded Coaching Operating System for CCP

*Document Type: Strategic Technical Decision Analysis*  
*Project: The Conscious Coaching Factory (CCP / Conscious Elite)*  
*Date: 2026-03-24*  
*Decision Scope: Replace Notion (ADR-02) with a self-hosted, white-labeled AFFiNE instance as the unified coach-facing and client-facing delivery layer.*

---

## I. Decision Context and Strategic Framing

The Conscious Coaching Platform currently relies on Notion as its primary Zero-UI delivery layer for coaches (codified in Architectural Decision Record ADR-02). This decision was originally justified by several sound reasoning points: Notion requires zero custom UI development, it is universally familiar to knowledge workers, and it strictly obeys the CCP's "Never Outshine the Master" principle by remaining invisible as infrastructure. However, the CCP ecosystem has since evolved far beyond its original Phase 0 scope, and three critical deficiencies in the Notion-based delivery model have become structurally impossible to ignore.

First, **Notion cannot be branded**. Every page, database, and embedded view that a coach interacts with carries the Notion watermark and aesthetic identity. For a platform that positions itself as the "definitive operating system for behavioral change infrastructure," presenting the coach's mission-critical operational cockpit inside another company's branded product creates an irreconcilable perception of dependency. It communicates that CCP is a Notion add-on, not a sovereign platform.

Second, **Notion cannot serve clients**. The current architecture restricts Notion access exclusively to the coach. Clients interact solely through Telegram (CBCS) and social media. But the vision of the Conscious Elite platform demands a future state where clients can access their own transformation dashboards, review their progress telemetry, revisit curated content libraries, and co-create within coach-guided workspaces. Notion's permission model and pricing structure make this economically and architecturally infeasible at scale.

Third, **Notion fractures the creative toolchain**. Coaches currently toggle between Notion (for content delivery and dashboards), Excalidraw (for visual diagramming and slide creation), external calendar tools (for content scheduling), and separate interfaces for reviewing CBCS conversation histories and CPSC sales data. This fragmentation directly violates the CCP core principle of Zero-Friction Efficacy. Every context switch is cognitive tax. Every additional login is a friction point that erodes platform stickiness.

AFFiNE, an MIT-licensed open-source workspace platform built by ToEverything, presents itself as a structurally superior alternative. It merges documents, whiteboards, databases, and presentation slides into a single edgeless canvas powered by BlockSuite (a CRDT-based collaborative editor framework), OctoBase (a Rust-powered local-first database engine), and a React/Electron frontend. It is fully self-hostable via Docker, supports real-time collaboration, and operates under a local-first data sovereignty model that aligns perfectly with CCP's single-tenant architecture (ADR-01).

This MCDA evaluates whether replacing Notion with a self-hosted, CCP-branded AFFiNE instance is strategically sound, technically feasible, and economically justified.

---

## II. Criteria Definition and Weighting

The following ten criteria have been selected to evaluate the integration. Each criterion is weighted on a scale of 1-10 based on its strategic importance to the CCP ecosystem. Scores are assigned on a 1-5 scale (1 = critically deficient, 5 = exceptional fit).

| # | Criterion | Weight (1-10) | Rationale for Weight |
|---|-----------|:---:|---|
| C1 | **Brand Sovereignty** | 10 | CCP must feel like a sovereign platform, not a Notion wrapper. |
| C2 | **Client Access Capability** | 9 | Enabling client-facing dashboards is a fundamental scaling unlock. |
| C3 | **Unified Creative Toolchain** | 9 | Eliminating tool fragmentation (Excalidraw, calendars, dashboards) directly impacts coach adoption. |
| C4 | **Self-Hosting & Data Sovereignty** | 8 | Single-tenant isolation (ADR-01) and AWS deployment compatibility are non-negotiable. |
| C5 | **Integration Surface Area** | 8 | The platform must expose APIs or extension points for CCP backend systems (CCF, CBCS, CPSC, CMF). |
| C6 | **Real-Time Collaboration** | 7 | Coaches and their teams need simultaneous editing, especially for V2WS webinar preparation. |
| C7 | **Deployment & Maintenance Burden** | 7 | With $0.51 in the bank and startup credits, operational overhead must be minimal. |
| C8 | **Learning Curve & Coach Adoption** | 6 | Coaches are not developers. The interface must be immediately intuitive. |
| C9 | **Long-Term Ecosystem Viability** | 6 | The upstream project must be actively maintained with a credible long-term trajectory. |
| C10 | **Cost Structure** | 5 | Direct monetary cost relative to Notion's per-seat pricing at scale. |

---

## III. Comparative Scoring: Notion vs. Self-Hosted AFFiNE

### C1: Brand Sovereignty (Weight: 10)

**Notion: 1/5.** Notion is indelibly Notion-branded. Every URL, every sidebar, every sharing link broadcasts the Notion identity. There is no mechanism to remove it. The coach sees "notion.so" in every URL. This permanently positions CCP as a layer running inside someone else's product.

**AFFiNE (Self-Hosted): 5/5.** Because the Community Edition is MIT-licensed and fully self-hosted, CCP has complete control over the deployment domain (`app.consciouselite.com`), the favicon, the login screen, the color palette, and every visible surface. The fork strategy allows us to replace all AFFiNE branding with Conscious Elite identity at the theme and asset level without modifying core functionality. The coach logs into *our* platform, not a third-party tool.

### C2: Client Access Capability (Weight: 9)

**Notion: 2/5.** Notion technically supports guest access, but at enterprise scale, guest seats become expensive ($10/guest/month on Team plans). More critically, the permission model is coarse: guests either see entire pages or nothing. There is no mechanism to dynamically surface personalized client dashboards driven by Neo4j telemetry data.

**AFFiNE (Self-Hosted): 4/5.** Self-hosting gives us total control over the authentication layer. We can implement custom SSO, Telegram-based login, or even anonymous read-only access for specific client workspaces. The CRDT-based architecture (via YJS) natively supports granular, real-time collaborative editing. We can build a custom permission middleware that maps Neo4j relationship depth to workspace visibility, fulfilling the CPSC's psychologically-gated access model. The score is 4 rather than 5 because this permission middleware would need to be custom-built; AFFiNE does not ship it out of the box.

### C3: Unified Creative Toolchain (Weight: 9)

**Notion: 2/5.** Notion has no native whiteboard or diagramming tool. Excalidraw must be used separately for V2WS slide composition. Content calendars require database views that lack visual timeline sophistication. There is no native slide presentation mode.

**AFFiNE (Self-Hosted): 5/5.** This is AFFiNE's strongest structural advantage. The Edgeless Canvas mode provides a full infinite whiteboard that directly competes with Miro and Excalidraw. Documents can toggle between Page Mode and Edgeless Mode, meaning a V2WS webinar script can simultaneously exist as a structured document and a visual slide deck. Multi-view databases support Kanban boards (for CCF Content Calendars), tables (for CPSC campaign tracking), and linked documents. AFFiNE natively replaces Notion, Excalidraw, and potentially even the separate content calendar interface in a single environment. This consolidation alone is a category-defining advantage for coach adoption.

### C4: Self-Hosting & Data Sovereignty (Weight: 8)

**Notion: 1/5.** Notion is exclusively cloud-hosted. All data resides on Notion's infrastructure. There is no self-hosting option. This directly conflicts with CCP's ADR-01 (Single-Tenant Architecture) and creates a hard dependency on a third-party vendor for the most sensitive coaching data.

**AFFiNE (Self-Hosted): 5/5.** AFFiNE ships with official Docker Compose configurations for self-hosting. It requires PostgreSQL (which we already run via Supabase) and Redis (which we already use for Voice DNA caching). Deploying it on our AWS infrastructure via Dockploy is architecturally trivial and maintains perfect data sovereignty within our single-tenant isolation boundary.

### C5: Integration Surface Area (Weight: 8)

**Notion: 3/5.** Notion has a well-documented REST API for creating pages, updating databases, and querying content. CCP already uses this API for Zero-UI delivery. However, the API is rate-limited (3 requests/second), does not support real-time event subscriptions (webhooks are limited), and cannot push live data updates to the coach's screen without polling.

**AFFiNE (Self-Hosted): 4/5.** Because we control the entire codebase, we can inject custom API endpoints directly into the AFFiNE server. The BlockSuite framework is designed for extensibility via custom blocks. We can create CCP-native blocks: a "CBCS Conversation Thread" block that renders a client's Telegram history inline, a "CPSC Pipeline" block that visualizes the sales funnel, a "CMF Preview" block that embeds a rendered video thumbnail with playback controls. The plugin architecture is still maturing (officially "coming soon"), but because we own the fork, we can implement custom blocks as first-party extensions without waiting for the upstream plugin API to stabilize. The score is 4 rather than 5 because this integration layer must be engineered; it is not declarative or zero-code.

### C6: Real-Time Collaboration (Weight: 7)

**Notion: 4/5.** Notion's real-time collaboration is excellent. Multiple users can edit simultaneously with cursor presence and conflict resolution.

**AFFiNE (Self-Hosted): 4/5.** AFFiNE uses YJS CRDTs (via y-octo, a high-performance Rust implementation) for real-time collaboration. This is architecturally identical to Notion's approach and, in some cases, superior due to the local-first data model, which allows offline editing with automatic conflict resolution upon reconnection. The December 2024 release added Team Workspace 1.0 with enhanced collaboration features.

### C7: Deployment & Maintenance Burden (Weight: 7)

**Notion: 5/5.** Zero deployment, zero maintenance. Notion is a fully managed SaaS.

**AFFiNE (Self-Hosted): 3/5.** Self-hosting introduces operational responsibility: Docker container management, database backups, SSL certificates, version upgrades, and monitoring. However, deploying via Dockploy on our existing AWS instance significantly reduces this burden. Dockploy handles reverse proxying, SSL via Let's Encrypt, and container lifecycle management. The ongoing maintenance cost is estimated at 2-4 hours per month for updates and monitoring, which is acceptable given the strategic benefits. The score reflects the non-trivial but manageable operational overhead.

### C8: Learning Curve & Coach Adoption (Weight: 6)

**Notion: 4/5.** Notion is universally known. Most coaches have at least basic familiarity.

**AFFiNE (Self-Hosted): 3/5.** AFFiNE's interface is structurally similar to Notion (block-based editing, slash commands, drag-and-drop) but is not identical. The Edgeless Canvas mode introduces a whiteboard paradigm that some coaches may find disorienting initially. However, because we control the deployment, we can pre-populate each coach's workspace with branded templates, pre-built dashboards, and guided onboarding sequences. The learning curve is a temporary friction point that diminishes rapidly with proper template engineering. The fact that we can hide unnecessary features and present a curated, coach-specific interface mitigates this risk significantly.

### C9: Long-Term Ecosystem Viability (Weight: 6)

**Notion: 5/5.** Notion is a multi-billion-dollar company with guaranteed long-term viability.

**AFFiNE (Self-Hosted): 4/5.** AFFiNE has 45,000+ GitHub stars, 233+ contributors, 545+ releases, and is backed by ToEverything with active development. The MIT license ensures that even if the upstream project stagnates, our fork remains fully functional and legally unencumbered. The Enterprise Edition (with SSO and advanced admin) is planned but not yet released, indicating the company is actively pursuing commercial sustainability. The CRDT-based architecture (BlockSuite + y-octo) represents cutting-edge collaborative infrastructure, which attracts ongoing developer attention.

### C10: Cost Structure (Weight: 5)

**Notion: 2/5.** Notion's Team plan costs $10/member/month. At 50 coaches, this is $500/month. Adding client access as guests would multiply this cost dramatically. At scale (500 coaches + 5,000 clients), Notion becomes prohibitively expensive.

**AFFiNE (Self-Hosted): 5/5.** The MIT-licensed Community Edition has zero per-seat costs. The only expense is the AWS compute hosting (which we are already provisioning for the CCP backend) and the engineering time for theming and custom block development. At scale, the marginal cost per additional coach or client workspace approaches zero.

---

## IV. Weighted Score Matrix

| Criterion | Weight | Notion Score | Notion Weighted | AFFiNE Score | AFFiNE Weighted |
|-----------|:------:|:---:|:---:|:---:|:---:|
| C1: Brand Sovereignty | 10 | 1 | 10 | 5 | 50 |
| C2: Client Access | 9 | 2 | 18 | 4 | 36 |
| C3: Unified Toolchain | 9 | 2 | 18 | 5 | 45 |
| C4: Data Sovereignty | 8 | 1 | 8 | 5 | 40 |
| C5: Integration Surface | 8 | 3 | 24 | 4 | 32 |
| C6: Real-Time Collab | 7 | 4 | 28 | 4 | 28 |
| C7: Deployment Burden | 7 | 5 | 35 | 3 | 21 |
| C8: Learning Curve | 6 | 4 | 24 | 3 | 18 |
| C9: Long-Term Viability | 6 | 5 | 30 | 4 | 24 |
| C10: Cost Structure | 5 | 2 | 10 | 5 | 25 |
| **TOTALS** | **75** | | **205** | | **319** |

**AFFiNE Weighted Total: 319 / 375 (85.1%)**  
**Notion Weighted Total: 205 / 375 (54.7%)**

**Delta: +114 points (+55.6% improvement)**

---

## V. Risk Analysis and Mitigation

### Risk 1: White-Label Branding Depth
AFFiNE's Community Edition does not ship with explicit white-label configuration flags. Branding changes (logos, colors, favicon, domain) require modifying the fork's theme assets and rebuilding the Docker image. **Mitigation:** This is a one-time engineering effort (estimated 8-16 hours). Once the branded Docker image is built, it deploys identically to the upstream. We create a `conscious-elite-theme` overlay that hooks into AFFiNE's existing CSS variable system and asset pipeline.

### Risk 2: Plugin API Immaturity
The BlockSuite plugin system is still officially "coming soon." Custom CCP blocks (CBCS viewer, CPSC pipeline, CMF preview) cannot rely on a stable plugin API. **Mitigation:** Because we own the fork, we implement custom blocks directly in the BlockSuite source as first-party components. This bypasses the plugin API entirely and gives us full TypeScript-level control over rendering, data fetching, and event handling. The trade-off is increased merge complexity when pulling upstream updates, but this is manageable via a disciplined rebasing strategy.

### Risk 3: Operational Overhead
Self-hosting introduces server management, backup responsibilities, and upgrade cycles that Notion eliminates entirely. **Mitigation:** Dockploy abstracts most of this complexity. The AFFiNE Docker Compose stack (PostgreSQL + Redis + AFFiNE server) is identical to infrastructure we are already provisioning for the CCP backend. We consolidate rather than multiply our operational footprint. Automated backup scripts to S3 and health-check monitoring via AWS CloudWatch provide enterprise-grade reliability.

### Risk 4: Upstream Divergence
If AFFiNE's upstream development diverges significantly from our fork's modifications, merging becomes increasingly expensive. **Mitigation:** We adopt a "thin fork" strategy: minimize changes to the core AFFiNE source. All CCP-specific customizations are implemented as: (a) theme overrides in a separate directory, (b) custom blocks registered via the existing block registration API, and (c) a custom authentication middleware layer. This isolates our changes from the upstream codebase and preserves merge compatibility.

---

## VI. Verdict and Recommendation

The MCDA produces a decisive, mathematically unambiguous result: **AFFiNE is the structurally superior platform for the CCP ecosystem by a margin of 55.6%.**

The integration transforms CCP from a backend intelligence layer that happens to dump outputs into Notion, into a **fully sovereign, branded coaching operating system** where every interaction—content creation, webinar composition, client relationship management, sales pipeline visualization, and video review—occurs inside a single, CCP-branded environment that the coach perceives as *ours*.

### Recommended Integration Strategy: Thin Fork + Theme Overlay

We recommend **forking AFFiNE and deploying it as a branded, self-hosted instance** on the existing AWS infrastructure via Dockploy. The fork follows a "thin fork" discipline:

1. **Theme Layer:** Replace all visual branding (logo, color palette, favicon, login screen, domain) via a CSS/asset overlay.
2. **Custom Blocks (Phase 1):** Build 4-6 CCP-native blocks (CBCS Conversation Viewer, CPSC Pipeline Board, CCF Content Calendar, CMF Video Preview, V2WS Slide Editor integration).
3. **Authentication Layer:** Implement custom SSO that ties into CCP's existing user management, enabling both coach and client login.
4. **Template Library:** Pre-populate every new coach workspace with CCP-branded templates for all operational modules.

This strategy preserves upstream compatibility while delivering a fully branded, client-accessible, unified coaching platform that no competitor in the market can replicate.

The decision is clear: **Proceed with AFFiNE integration. Retire ADR-02 (Notion as Delivery Layer). Issue ADR-05: AFFiNE as the Conscious Elite Coaching OS.**

---
*End of MCDA. Prepared for CCP Architectural Review.*
