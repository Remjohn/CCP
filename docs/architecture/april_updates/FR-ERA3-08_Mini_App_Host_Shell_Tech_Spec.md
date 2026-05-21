# Tech-Spec: FR-ERA3-08 — Mini App Host Shell
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 Architecture — CBAR-Hardened)
**Phase:** 1 — Infrastructure
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md §7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms the existing API gateway is `src/ccp/api/main.py`, but this spec's
                      prompt-specific context explicitly forbids adding new endpoints there because the Host Shell
                      is a frontend container using the Telegram WebApp SDK.
2. PRD LOADED:        PRD-01 exact brownfield definition: "Establish the foundational platform split: **AFFiNE**
                      serves as the Sovereign Command Center for the coach ... **Telegram** (via chat and native
                      Mini Apps) serves as the Sovereign Execution Surface for the client/audience..."
                      PRD-04 exact surface definition: "The Telegram Mini App and native Telegram chat should work
                      together rather than compete." PRD-04 further specifies: "The Mini App should handle: richer
                      interaction surfaces, score visualizations, reaction recording states, vote and share flows,
                      challenge progression surfaces, playful or branded visual logic."
3. EPIC LOADED:       Phase 1 Epic 1 Story 1.1 first AC: "Given I tap a Web App button in Telegram, When the
                      shell loads, Then it renders the System 1 UI optimistically without blocking for network
                      responses, And it validates the `initData` hash against the bot token asynchronously in the
                      background."
4. CBAR AUDIT LOADED: Phase1-M01 (Optimistic Render Rule), Phase1-M02 (Zero-Network Theme Rule), and Phase1-M03
                      (Primer Screen Rule) confirmed from the Phase 1 audit. The hallucination purge also corrects
                      the false `EXP-TRB-004` reference to verified `EXP-TRS-001`.
5. PRIMITIVES LOADED: `experience_primitive_id: "EXP-FRC-002"` / `canonical_name: "System 1 to System 2 Escalation"`
                      `experience_primitive_id: "EXP-TRS-001"` / `canonical_name: "Visceral Hooking (Premium Authority Aesthetic)"`
                      `experience_primitive_id: "EXP-FRC-003"` / `canonical_name: "The B=MAP Friction Audit"`
6. BACKEND FILES READ:`src/ccp/services/dpa_engine.py` - `async def resolve(self, coach_id: str, content_archetype: str, audience_mood_state: str = "", brand_hue_analysis: BrandHueAnalysis | None = None, override_mode: OverrideMode = OverrideMode.adaptive, identity_tokens: dict[str, Any] | None = None) -> DPAResult`
7. TEST PATTERN:      `tests/integration/test_cpsc_fr52_webinar_brief.py` and
                      `tests/integration/test_ca11_fr16_studio_block.py` use helper builders, scenario-oriented
                      classes, direct field assertions, and concrete lifecycle checks rather than generic smoke tests.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P1_S01_FR-ERA3-08_Mini_App_Host_Shell.md` | 2026-05-11 | Assignment prompt, frontend-only constraint, and exact output target |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Required architecture format, stack inventory, and CBAR documentation structure |
| 3 | `docs/architecture/april_updates/Phase1_Infrastructure_Epics.md` | 2026-05-10 | Epic 1 stories 1.1, 1.2, and 1.3 plus all three Host Shell mandates |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase1_Infrastructure.md` | 2026-05-10 | M-01, M-02, M-03 resolution demands and primitive hallucination purge |
| 5 | `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` | v6.0, 2026-05-06 | Two-surface platform split and Telegram Mini App execution-surface doctrine |
| 6 | `docs/prd/modules/PRD_04_CVE_Experience_Design.md` | v6.0, 2026-05-06 | Mini App platform role, state continuity, and richer interaction requirements |
| 7 | `primitives/experience/friction_ability/EXP-FRC-002.yaml` | Codified registry | Verified optimistic/low-friction initialization primitive |
| 8 | `primitives/experience/trust_branding/EXP-TRS-001.yaml` | Codified registry | Verified premium visual authority primitive |
| 9 | `primitives/experience/friction_ability/EXP-FRC-003.yaml` | Codified registry | Verified permission and deep-link friction-audit primitive |
| 10 | `src/ccp/services/dpa_engine.py` | Existing service | Resolved palette generation boundary used upstream of the shell |
| 11 | `src/ccp/models/ca11_models.py` | Existing models | `ResolvedPalette` and `DPAResult` contract source |
| 12 | `tools/tierlist-app/package.json` | Existing frontend baseline | Vite + React package structure already present in repo |
| 13 | `tools/tierlist-app/src/main.jsx` | Existing frontend baseline | Minimal React bootstrap entrypoint pattern |
| 14 | `tools/tierlist-app/src/App.jsx` | Existing frontend baseline | Existing Vite shell layout pattern and current React style choices |
| 15 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Helper-builder and scenario-based pytest pattern |
| 16 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Concrete status/lifecycle assertion pattern for richer specs |

## 2. Overview

### 2.1 Problem Statement

CCP now depends on Telegram Mini Apps as the audience-side execution surface, but there is still no shared host shell that every Mini App can rely on for consistent startup, theme application, and deep-link routing.

Without a dedicated host shell, three concrete failures appear immediately:

- initialization blocks on authentication or theme fetches, creating a cold blank state before the user sees anything
- each Mini App reinvents startup logic, causing inconsistent branding, permission handling, and routing semantics
- hardware-dependent surfaces trigger OS prompts without context, creating abrupt friction and abandonment

Epic 1 is specifically preventing those failures. The shell must render optimistically, apply the coach theme without any network call, and route to the exact requested surface while inserting a high-emotion primer when permissions are needed.

### 2.2 Solution

This spec defines a reusable Vite + React Mini App Host Shell under a new frontend workspace. The shell consumes Telegram `startapp` payloads plus the Telegram WebApp JavaScript SDK, decodes a precomputed `ResolvedPalette` locally, boots a global DPA theme layer, resolves the target surface, performs permission gating, and mounts the requested Mini App module inside a shared branded frame. It does not fetch runtime theme data, does not add FastAPI endpoints, and does not treat Telegram identity as a traditional login flow.

### 2.3 Scope

**In scope:**

- reusable Vite + React host shell workspace
- Telegram WebApp SDK bootstrap and context extraction
- local decoding of `startapp` payloads
- optimistic first render before async validation completes
- zero-network DPA theme application via CSS custom properties
- dynamic deep-link routing to named Mini App surfaces
- permission primer screens for microphone and camera gated surfaces
- frontend state model for bootstrap, validation, theme, permissions, and route lifecycle
- shared error / degraded shell fallback for invalid payloads or validation failure
- adding a dedicated `POST /api/miniapp/validate-init` endpoint to `src/ccp/api/main.py` for asynchronous hash verification

**Out of scope:**

- fetching theme data from the backend after shell launch
- reimplementing Telegram message ingress in `telegram_webhook.py`
- building the internals of each surface module such as Solo, Debate, Webinar Companion, or payments
- replacing `DPAEngine.resolve()` with frontend theme generation logic
- adding standalone browser auth or email/password flows

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Data Object | Source FR | What It Does |
|---|---|---|---|
| DEP-MSH-001 | `MiniAppStartappPayload` | Story 1.1 | The encoded initialization payload passed via Telegram `startapp` parameter |
| DEP-MSH-002 | `MiniAppRoutePacket` | Story 1.3 | The decoded routing instruction defining target surface and permission requirements |
| DEP-MSH-003 | `MiniAppResolvedPalettePacket` | Story 1.2 | The frontend-safe theme payload decoded for zero-network CSS application |
| DEP-MSH-004 | `MiniAppIdentityToken` | Story 1.1 | The coach's brand identity variables (logo, typography) |
| DEP-MSH-005 | `MiniAppPaletteColors` | Story 1.2 | The specific hex values and gradients applied to CSS variables |
| DEP-MSH-006 | `MiniAppBootstrapState` | Story 1.1 | The central frontend state machine for initialization, validation, and permissions |
| DEP-MSH-007 | `MiniAppSurfaceKey` | Story 1.3 | Enum defining the allowed routing targets |
| DEP-MSH-008 | `PermissionRequirement` | Story 1.3 | Enum defining hardware access states |

### 3.2 Existing Backend Integration

| File / Resource | Path | How This Spec Uses It |
|---|---|---|
| `dpa_engine.py` | `src/ccp/services/dpa_engine.py` | Uses the shape and semantics of `DPAEngine.resolve(...)` outputs as the authoritative source for precomputed theme payloads. The shell never recomputes palettes. |
| `ca11_models.py` | `src/ccp/models/ca11_models.py` | Reuses `ResolvedPalette` field semantics to define the frontend-safe encoded theme contract. |
| `telegram_webhook.py` | `src/ccp/api/telegram_webhook.py` | Explicit non-dependency at runtime. This shell does not call the webhook for initialization or identity. Mentioned to prevent accidental reinvention of Telegram auth. |
| `tools/tierlist-app/package.json` | `tools/tierlist-app/package.json` | Existing local Vite + React pattern used as the baseline workspace structure reference. |
| `tools/tierlist-app/src/main.jsx` | `tools/tierlist-app/src/main.jsx` | Existing minimal React bootstrap pattern reused for shell entrypoint conventions. |
| `tools/tierlist-app/src/App.jsx` | `tools/tierlist-app/src/App.jsx` | Existing repo-local React app structure reference for layout organization only; not reused as product logic. |

**Existing DB tables used indirectly upstream, not at shell runtime:**

- `resolved_palettes`
  Why: the backend DPA engine may persist palette audit trails here before generating startapp payloads.
- `person_registry`
  Why: identity is still resolved server-side elsewhere in CCP, but the shell does not query it during launch.

**Existing API routes deliberately not used during shell initialization:**

- `POST /api/telegram/webhook`
- `GET /health`

**New frontend workspace introduced by this spec:**

- `tools/miniapp-host-shell/`

**New API routes introduced by this spec:**

- `POST /api/miniapp/validate-init` (Added to securely validate the `initData` hash against the Bot Token without exposing it to the frontend.)

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-FRC-002` | System 1 to System 2 Escalation | friction_ability | The shell must render immediately from local context and defer validation work into the background. No blocking spinner-first boot flow is allowed. |
| `EXP-TRS-001` | Visceral Hooking (Premium Authority Aesthetic) | trust_branding | Theme application must establish premium branded authority within milliseconds, with no generic flash of unstyled content. |
| `EXP-FRC-003` | The B=MAP Friction Audit | friction_ability | Deep links must eliminate unnecessary navigation and permission prompts must be primed contextually before OS-level friction appears. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story Origin | Implementation Mechanism |
|---|---|---|---|
| Optimistic Render Rule | Phase1-M01 | Story 1.1 | `OptimisticBootController` mounts the shell frame, background color, typography skeleton, and route placeholder immediately from local `startapp` + Telegram context while `InitDataValidationAgent` runs asynchronously. |
| Zero-Network Theme Rule | Phase1-M02 | Story 1.2 | `StartappPayloadDecoder` extracts an encoded theme packet, and `GlobalDPAThemeProvider` sets CSS variables synchronously during app bootstrap before the first paint. |
| Primer Screen Rule | Phase1-M03 | Story 1.3 | `PermissionGateResolver` intercepts mic/camera routes and sends ungranted cases to `PrimerScreenComposer` before any OS permission call is triggered. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Host shell lives in a dedicated workspace `tools/miniapp-host-shell/` | Multiple Mini Apps need one shared container, and the prompt explicitly frames this as a host shell rather than a single tool app. | Reuse `tools/tierlist-app/` as the shared shell | Existing Tierlist app is a feature-specific app and later specs explicitly avoid reusing it as a generic host. |
| Theme arrives via encoded `startapp` payload | Phase1-M02 requires zero-network theme resolution. | Fetch `ResolvedPalette` from backend on mount | Violates M-02 and causes blank/generic flash. |
| Init validation is async after first paint | Phase1-M01 requires optimistic first render. | Block all rendering until `initData` is validated | Violates M-01 and creates immediate friction. |
| Permission primer is an explicit route state | M-03 requires emotional priming before hardware prompts. | Call `navigator.mediaDevices.getUserMedia()` immediately on surface deep-link | Violates M-03 by showing a cold OS prompt. |
| Shared shell state is a deterministic local store | Boot state is finite and cross-cutting: payload, validation, permissions, route. | Let each child surface manage bootstrap individually | Creates drift and repeated infra bugs across apps. |
| Frontend contract models are still codified in `src/ccp/models/` | The protocol requires typed primary schemas even for frontend-producing specs. | Leave payload shape undocumented in prose only | Too ambiguous for upstream URL builders and downstream React shell implementers. |

## 4. Implementation Plan

### Phase 1 — Workspace Scaffold and Bootstrap

- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\package.json` using the repo-local Vite + React baseline from `tools/tierlist-app/package.json`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\vite.config.js` with a Telegram Mini App-compatible single-page build target.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\index.html` with a non-white bootstrap background and root mount.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\main.jsx` to mount `MiniAppHostShell`.

### Phase 2 — Shell State and Theme Contract

- [ ] Create `D:\Work\The Conscious Coaching Factory\src\ccp\models\mini_app_shell_models.py` with typed startapp/theme/bootstrap models from Section 5.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\StartappPayloadDecoder.js` for local payload decoding.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\MiniAppShellStateStore.js` for deterministic shell state.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\GlobalDPAThemeProvider.jsx` to apply CSS custom properties before first paint, and explicitly map backend metadata (`bhcs`, `kelvin_range`, `saturation_adjustment`, `override_active`) to root HTML `data-*` attributes for downstream JS logic.

### Phase 3 — Validation and Routing

- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\TelegramBootstrapAdapter.js` to read the Telegram WebApp SDK and launch parameters.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\OptimisticBootController.jsx` to render immediately using local boot data.
- [ ] Create `D:\Work\The Conscious Coaching Factory\src\ccp\api\miniapp_auth.py` to expose the `POST /api/miniapp/validate-init` endpoint.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\InitDataValidationAgent.js` to asynchronously call `POST /api/miniapp/validate-init` and run validation downgrade logic.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\SurfaceRegistryRouter.jsx` to map `startapp` surface keys to lazy-loaded modules.

### Phase 4 — Permission Priming and Fallback

- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\PermissionGateResolver.js` for hardware requirement checks.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\PrimerScreenComposer.jsx` for microphone/camera primer experiences.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\ShellFallbackScreen.jsx` for invalid payload, unsupported surface, and validation-downgrade states.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\ShellChrome.jsx` for consistent safe-area and branded container layout.

### Phase 5 — Test and QA Harness

- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\test\fixtures\startappPayloads.json` with valid, invalid, and permission-gated examples.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\test\shellBootstrap.spec.jsx` for unit tests around decode, route, and permission gating.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\README.md` documenting payload shape, route registration, and launch assumptions.
- [ ] Add manual QA checklist items to `D:\Work\The Conscious Coaching Factory\docs\architecture\april_updates\FR-ERA3-08_Mini_App_Host_Shell_Tech_Spec.md` Section 10 and keep them in sync with implementation.

## 5. Primary Output Schema

**New model file:** `D:\Work\The Conscious Coaching Factory\src\ccp\models\mini_app_shell_models.py`

```python
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class MiniAppSurfaceKey(str, Enum):
    """DEP-MSH-007"""
    react_solo = "react_solo"
    react_debate = "react_debate"
    react_duel = "react_duel"
    react_tierlist = "react_tierlist"
    react_mirror_quiz = "react_mirror_quiz"
    react_blind_rank = "react_blind_rank"
    react_alphabet = "react_alphabet"
    react_elimination = "react_elimination"
    react_authority_quiz = "react_authority_quiz"
    react_ranking_quiz = "react_ranking_quiz"
    webinar_companion = "webinar_companion"
    scorecard_viewer = "scorecard_viewer"


class PermissionRequirement(str, Enum):
    """DEP-MSH-008"""
    none = "none"
    microphone = "microphone"
    camera = "camera"
    microphone_and_camera = "microphone_and_camera"


class MiniAppIdentityToken(BaseModel):
    """DEP-MSH-004"""
    coach_acronym: str = Field(..., min_length=2, max_length=4)
    display_name: str = Field(default="", max_length=80)
    logo_url: str = Field(default="", max_length=500)
    font_family: str = Field(default="", max_length=120)


class MiniAppPaletteColors(BaseModel):
    """DEP-MSH-005"""
    background_primary: str = Field(..., pattern=r"^#(?:[0-9a-fA-F]{6})$")
    background_gradient: str = Field(..., min_length=1, max_length=160)
    accent: str = Field(..., pattern=r"^#(?:[0-9a-fA-F]{6})$")
    text_primary: str = Field(..., pattern=r"^#(?:[0-9a-fA-F]{6})$")
    text_secondary: str = Field(..., pattern=r"^#(?:[0-9a-fA-F]{6})$")
    overlay: str = Field(..., pattern=r"^#(?:[0-9a-fA-F]{6})$")


class MiniAppResolvedPalettePacket(BaseModel):
    """DEP-MSH-003"""
    resolved_palette_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    content_archetype: str = Field(..., min_length=1)
    audience_mood_state: str = Field(default="", max_length=80)
    bhcs: float = Field(..., ge=0.0, le=1.0)
    brand_hue_used: bool = Field(default=False)
    kelvin_range: str = Field(default="", max_length=80)
    saturation_adjustment: float = Field(default=0.0, ge=-1.0, le=1.0)
    override_active: bool = Field(default=False)
    identity: MiniAppIdentityToken
    palette: MiniAppPaletteColors


class MiniAppRoutePacket(BaseModel):
    """DEP-MSH-002"""
    surface: MiniAppSurfaceKey
    permission_requirement: PermissionRequirement = Field(default=PermissionRequirement.none)
    primer_headline: str = Field(default="", max_length=120)
    primer_body: str = Field(default="", max_length=280)


class MiniAppStartappPayload(BaseModel):
    """DEP-MSH-001"""
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    launch_id: str = Field(..., min_length=1)
    route: MiniAppRoutePacket
    resolved_palette: MiniAppResolvedPalettePacket
    optimistic_title: str = Field(..., min_length=1, max_length=120)
    optimistic_subtitle: str = Field(default="", max_length=160)


class MiniAppBootstrapPhase(str, Enum):
    prepaint = "prepaint"
    optimistic_ready = "optimistic_ready"
    validating = "validating"
    active_surface = "active_surface"
    primer = "primer"
    degraded = "degraded"


class MiniAppBootstrapState(BaseModel):
    """DEP-MSH-006"""
    phase: MiniAppBootstrapPhase
    surface: MiniAppSurfaceKey
    permission_requirement: PermissionRequirement
    validation_pending: bool = Field(default=True)
    validation_failed: bool = Field(default=False)
    sdk_present: bool = Field(default=False)
```

**Schema notes:**

- These models codify the frontend contract that upstream Telegram button builders must satisfy.
- The shell decodes an encoded `MiniAppStartappPayload` from `startapp`; it does not perform a runtime fetch to fill missing fields.
- `ResolvedPalette` is flattened into a frontend-safe packet with no `Any` types.

## 6. Backward Compatibility Fallback

The host shell must degrade gracefully in the same spirit as `circuit_breaker.py`: fail safe, not blank.

| Failure Mode | Fallback Behavior |
|---|---|
| Telegram WebApp SDK unavailable | Render `ShellFallbackScreen` with a branded unsupported-environment message and no hard crash. |
| `startapp` payload missing or undecodable | Render a branded invalid-launch state with a single recovery instruction instead of a blank page. |
| Async `initData` validation fails after optimistic render | Downgrade the shell to a restricted read-only or retry state, preserving the themed frame and explanatory messaging. |
| Permission API unsupported | Route to primer screen and expose an explicit manual "Continue" permission trigger rather than auto-firing unsupported checks. |
| Unknown surface key | Render the shell chrome and a route-unavailable fallback card; do not redirect to a generic home menu. |

**Hard fallback rules:**

- Never flash an unthemed white or system-default background.
- Never replace the optimistic shell with a raw browser error.
- Never block first render on a network retry path.

## 7. Tasks

- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\package.json`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\vite.config.js`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\index.html`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\main.jsx`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\App.jsx`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src/styles/shell.css`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\TelegramBootstrapAdapter.js`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\StartappPayloadDecoder.js`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\MiniAppShellStateStore.js`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\GlobalDPAThemeProvider.jsx`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\OptimisticBootController.jsx`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\InitDataValidationAgent.js`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\SurfaceRegistryRouter.jsx`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\PermissionGateResolver.js`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\PrimerScreenComposer.jsx`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\shell\ShellFallbackScreen.jsx`.
- [ ] Create `D:\Work\The Conscious Coaching Factory\src\ccp\models\mini_app_shell_models.py`.
- [ ] Add test files under `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\test\`.

## 8. Acceptance Criteria

### Story 1.1 — Secure Web App Initialization

**AC1**

- Given I tap a Web App button in Telegram
- When the shell loads
- Then the first experiential shell frame is visible before any asynchronous validation result resolves
- And the async validation workflow begins in the background within 250ms of bootstrap
- And the shell does not display a blocking spinner, blank canvas, or login wall
- CBAR Mandate enforced: `Phase1-M01`
- Measurable pass condition: first branded shell paint occurs without any network dependency and validation status is still `pending`
- FAILURE EXAMPLE: the app shows a blank screen or loading spinner while waiting for `initData` validation to finish

### Story 1.2 — Global DPA Theme Resolution

**AC2**

- Given the shell receives an encoded `startapp` payload containing a `ResolvedPalette`
- When bootstrap begins
- Then the shell decodes the palette locally
- And applies all global CSS variables before the first user-visible frame
- And performs zero runtime backend theme requests
- CBAR Mandate enforced: `Phase1-M02`
- Measurable pass condition: no fetch/XHR call is required for theme resolution and no generic theme flash appears
- FAILURE EXAMPLE: the shell first renders with a white background or neutral fallback colors while waiting for a backend theme request

### Story 1.3 — Dynamic Surface Routing

**AC3**

- Given a Telegram button contains a named surface key in `startapp`
- When the shell decodes the route packet
- Then it mounts the requested surface directly with zero intermediate home-menu clicks
- And if the target requires microphone or camera access, it evaluates permissions before mounting the live tool
- CBAR Mandate enforced: `Phase1-M03`
- Measurable pass condition: direct deep-link lands on requested surface or its primer route with no manual menu navigation
- FAILURE EXAMPLE: the user lands on a generic launcher menu and must choose the tool again

**AC4**

- Given the target surface needs hardware permissions and the permission state is unset
- When the shell processes the deep-link
- Then it routes to a branded primer screen before any OS permission dialogue is triggered
- And only after the user acts on the primer may the browser permission request fire
- CBAR Mandate enforced: `Phase1-M03`
- Measurable pass condition: `PrimerScreenComposer` renders before any `getUserMedia` or equivalent prompt call
- FAILURE EXAMPLE: the OS microphone prompt appears immediately on launch with no emotional framing or explanation

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|---|---|---|
| `src/ccp/services/dpa_engine.py` | Upstream palette producer | Precomputed `ResolvedPalette` semantics and field meanings |
| `src/ccp/models/ca11_models.py` | Shared model contract | Existing `ResolvedPalette` baseline that the shell payload mirrors safely |
| `docs/architecture/april_updates/Phase1_Infrastructure_Epics.md` | Product constraint source | Canonical AC and CBAR mandate wording |
| `tools/tierlist-app/` | Frontend structural reference | Existing repo-local Vite + React layout pattern |

### External

| API/Library | Version | Purpose |
|---|---|---|
| Telegram WebApp JavaScript SDK | Telegram current WebApp SDK | Launch context, viewport, haptics, and integration with Telegram Mini Apps |
| React | `18.3.1` | Host shell UI runtime |
| React DOM | `18.3.1` | DOM mounting |
| Vite | `6.0.0` | Frontend build and local dev server |
| `@vitejs/plugin-react` | `4.3.4` | React compilation support in Vite |

## 10. Testing Strategy

### Unit Tests

| Test File | Describe Block | Test Name | What It Verifies |
|---|---|---|---|
| `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\test\shellBootstrap.spec.jsx` | `StartappPayloadDecoder` | `decodes_resolved_palette_without_network_calls` | local payload decode produces full theme contract with no fetch dependency |
| `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\test\shellBootstrap.spec.jsx` | `OptimisticBootController` | `renders_optimistic_shell_before_validation_resolution` | first shell frame appears while validation remains pending |
| `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\test\shellBootstrap.spec.jsx` | `PermissionGateResolver` | `routes_to_primer_before_permission_prompt_when_unset` | cold OS permission prompts are prevented |
| `D:\Work\The Conscious Coaching Factory\tools\miniapp-host-shell\src\test\shellBootstrap.spec.jsx` | `SurfaceRegistryRouter` | `mounts_direct_surface_from_startapp_key` | deep-link goes straight to requested surface or fallback |

### Integration Tests

Modeled on:

- `D:\Work\The Conscious Coaching Factory\tests\integration\test_cpsc_fr52_webinar_brief.py`
- `D:\Work\The Conscious Coaching Factory\tests\integration\test_ca11_fr16_studio_block.py`

Named integration tests:

- `test_shell_boots_with_optimistic_render_and_pending_validation`
- `test_theme_packet_applies_css_variables_before_first_surface_mount`
- `test_permission_gated_route_shows_primer_before_requesting_microphone`

Pattern requirements:

- use small helper builders for valid and invalid `startapp` payloads
- assert concrete bootstrap phase transitions and CSS variable presence
- assert measurable booleans such as `validation_pending`, `sdk_present`, and `permission_requirement`

### Manual Verification

1. Open the Mini App from Telegram with a valid encoded `startapp` payload for a surface that requires no permissions.
2. Confirm the first visual frame is branded immediately and no loading spinner or blank white flash appears.
3. Confirm no runtime theme request is made during initialization.
4. Open the Mini App with a microphone-gated surface key.
5. Confirm the primer screen appears before the OS permission dialogue.
6. Grant permission and confirm the requested surface mounts directly.
7. Launch with a corrupted payload and confirm the shell fallback screen appears without crashing the app.
8. Simulate async validation failure and confirm the shell downgrades gracefully without losing branded chrome.
