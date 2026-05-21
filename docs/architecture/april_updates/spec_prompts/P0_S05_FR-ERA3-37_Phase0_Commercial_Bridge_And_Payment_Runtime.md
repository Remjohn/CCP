# Spec Prompt: FR-ERA3-37 - Phase-0 Commercial Bridge and Payment Runtime

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-37
SPEC_TITLE:      Phase-0 Commercial Bridge and Payment Runtime
PHASE:           0 - Trial Phase-0 Commercial Runtime
SOURCE_PRD:      PRD-01, PRD-09
MAPPED_STORIES:  free-proof to $29.99 activation, $29.99 credit bridge to $39.99/$99.99, Telegram-native payment handoff, activation-state gating
CBAR_MANDATES:   Proof-Before-Payment Rule, Clean-Credit-Bridge Rule, Telegram-Native Commercial Flow Rule, No-Random-Upsell Rule, Continuity-Bridge Rule
BACKEND_REL:     NEW commercial bridge runtime - MUST interoperate with existing billing/payment rails and state models without inventing a detached checkout architecture
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-37_Phase0_Commercial_Bridge_And_Payment_Runtime_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the commercial runtime that turns free proof into:
> - `$29.99` activation
> - credit-aware upgrade into `$39.99/mo`
> - credit-aware upgrade into `$99.99/mo`
>
> It must preserve the doctrine:
> - proof is visible
> - activation / ownership / unlock is paid
> - the `$29.99` is applied toward the first qualifying upgrade

> [!IMPORTANT]
> **MANDATORY PHASE-0 SOURCE SET - READ IN EVERY PHASE-0 SPEC SESSION:**
> - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
> - `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Pricing_Silent_Referral_CoCreation_Architecture.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-09`, `PRD-01`. **PROOF:** Quote the exact lines that establish the pricing ladder, Telegram-native continuity, and the `$29.99` credit bridge.
3. Phase-0 source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing backend references: read real billing, payment, checkout, and state-transition files. **PROOF:** Quote real method signatures.
5. Existing models: read payment, billing, offer-tier, unlock-state, and entitlement model files.
6. Existing test patterns: read 2 `tests/integration/` files covering payment or entitlement flows.
7. Existing continuity boundaries: confirm what remains Phase-0 only and what becomes continuity / Coach OS concern.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (>=8) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Commercial states / unlocks | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `Phase0CommercialState`
  - `FirstProofUnlockRequest`
  - `FirstProofUnlockReceipt`
  - `UpgradeCreditState`
  - `UpgradeOfferBridge`
  - `Phase0EntitlementState`
- Define what remains free vs what becomes unlocked after payment
- Define credit validity / application logic for upgrade paths
- Preserve the clean framing that this is continuation, not coupon clutter
- Define Telegram-native payment handoff and post-payment unlock propagation

**REJECTION:** generic checkout spec | no clear free-vs-paid gating | no upgrade credit state | no Telegram-native flow | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
