# Pricing Strategy Analysis: Weekly Self-Service vs Current Retainer Model

## Your Proposal vs Current Plan — Side by Side

| | **Current Plan (v5.0)** | **Your New Proposal** |
|---|---|---|
| **Entry point** | $25 one-time "Witness Edit" | $25/week (self-service access) |
| **Core offer** | $250/mo retainer (8 videos) | $50/week = $200/mo (12 shorts + 4 long + 4 courses + 24 visual) |
| **CBCS backend** | $4/user/mo | $4/user/mo *(unchanged)* |
| **Revenue per coach** | $250/mo | $100-200/mo |
| **Barrier to entry** | Medium (needs sales call) | **Very low** (just pay $25 and go) |
| **Growth speed** | Slow (1-on-1 sales) | **Fast** (self-service, word of mouth) |

---

## 🟢 What's BRILLIANT About This Shift

### 1. The $25 Entry Is Now a RECURRING Trojan Horse
Your original plan had $25 as a one-time "Witness Edit." Dead money. Now $25/week is **$100/mo recurring** that also gets them INTO the platform where agents pre-brand everything and start producing content. The friction-to-revenue ratio is way better.

### 2. "Pay What You Use" Perception Kills SaaS Fatigue
Your own Pillar #8 says *"we bypass SaaS Fatigue by offering credits."* Weekly pricing takes this further — coaches think in weeks, not months. $25/week feels like "a nice dinner" not "another subscription."

### 3. Telegram Does the Heavy Lifting = Lower CAC
Your insight is correct: once they're in the Telegram channel after the $25 payment, your agents can:
- Push data-driven content ideas
- Schedule next video production automatically
- Create "addiction" to the Voice-First interface
- **The platform sells the upgrade, not you**

### 4. Pre-Branded Platform = Instant Lock-In
If the platform is already branded for them when they enter (logo, colors, tone), they feel ownership immediately. Switching cost goes up before they even produce video #2.

---

## 🧠 The "Dinner Pricing" Psychology — Why This Kills Subscriptions

This is the core insight that makes weekly pricing **categorically different** from monthly retainers:

| Mental Category | Example | Friction Level |
|---|---|---|
| **"Subscription"** | $250/mo retainer, $99/mo SaaS | HIGH — coach evaluates ROI monthly, considers canceling |
| **"Transaction"** | $25 video edit, $44 dinner | LOW — it's a purchase, not a commitment |
| **"Utility"** | Grocery run, AWS bill | ZERO — automated, invisible, "just how it works" |

**Your $25/week sits in the "transaction" zone.** Like Fiverr — nobody thinks "I'm paying $200/month for Fiverr." They think "I'm buying a $25 gig." Then another. Then another. The psychology of per-transaction spending completely bypasses the "should I cancel?" audit that kills monthly SaaS.

> [!IMPORTANT]
> **The $44 dinner × 7/month = $308/month but nobody feels that.** This is precisely the effect. A coach paying $25/week is spending $100/month but it NEVER triggers the "is this worth $100?" mental audit. Each $25 is evaluated on its own: *"Is this one video worth $25?"* → Obviously yes.

### The Automated Payment Mandate

This leads directly to a **non-negotiable technical requirement:**

> [!CAUTION]
> **The $4/user CBCS credit MUST auto-charge the moment a coach onboards a new client.** If there's a manual step — an invoice, an approval, a "please confirm" — you bleed revenue. Every new end-user that enters without an automated $4 charge is money you never recover because you'll never go back and retroactively bill for it.

**Payment architecture must be:**
```
Coach pays $25/week → auto-recurring (Stripe subscription, weekly cycle)
Coach adds client  → $4/user auto-charges to coach's card on file (metered billing)
Coach upgrades     → $50/week swap, no friction, same card
```

**Stripe metered billing** does exactly this — you report usage (new client added) and Stripe bills at end of cycle. No invoice, no confirmation. The coach's card is already on file from the $25/week.

**This means the CBCS onboarding flow must:**
1. Auto-provision the Telegram bot for the new client
2. Auto-report the usage event to Stripe
3. Auto-charge at next billing cycle
4. Zero human intervention on either side

---

## 🟡 Tensions to Resolve

### 1. Revenue Math — You're Leaving Money on the Table (Short Term)

| Scenario | Coaches | Revenue/mo | CBCS (50 users each) | **Total** |
|---|---|---|---|---|
| **Current plan** | 24 @ $250/mo | $6,000 | 24 × 50 × $3 = $3,600 | **$9,600/mo** |
| **New $25/wk only** | 40 @ $100/mo | $4,000 | 40 × 50 × $3 = $6,000 | **$10,000/mo** |
| **New $50/wk only** | 24 @ $200/mo | $4,800 | 24 × 50 × $3 = $3,600 | **$8,400/mo** |
| **New mixed** | 20 @ $100 + 15 @ $200 | $5,000 | 35 × 50 × $3 = $5,250 | **$10,250/mo** |

> [!IMPORTANT]
> You need **more coaches** at the lower price to match current plan revenue. BUT — the lower barrier means you GET more coaches faster. The question is: **what's your conversion rate at $25/week vs $250/mo?**

The bet: If $25/week converts 3x more coaches than $250/mo retainer, you **win on volume AND on CBCS backend** because more coaches = more end-users = more $4/user credits.

### 2. Deliverable Load at $50/Week is MASSIVE

$50/week = $200/mo and you're promising:
- 12 short videos (3/week)
- 4 long videos (1/week)
- 4 course videos (1/week)
- 24 visual content pieces (6/week)
- Content scheduling + posting
- Metrics + Telegram follow-ups
- CBCS + CPSC access

> [!CAUTION]
> That's **44 content pieces/month per coach.** With 24 coaches = **1,056 pieces/month.** Your CMF pipeline MUST be fully automated — any manual touch at this volume breaks you. Compare: current plan is 8 videos/mo × 24 = 192 pieces. You're going **5.5x the volume** at a **lower price**.

**This is only viable if CMF is production-grade.** Otherwise you burn out or produce garbage.

### 3. The "Infect & Deploy" Funnel Needs Adjustment

Your current funnel: `$25 one-time → $250 retainer → CBCS deployment`

New funnel should be: `$25/week self-service → natural upgrade to $50/week → CBCS deployment`

The CBCS "Trojan Horse" trigger STILL works — they'll use the bot daily at $25/week and realize their clients need it too. If anything, this is **faster** because more coaches are using the bot at the lower tier.

---

## 🔴 Critical Decision: Hybrid or Full Replacement?

### Option A: Full Replacement (Kill the $250/mo retainer)
- **Pro:** Simple pricing, easy to market, self-service scales
- **Con:** Existing clients feel devalued, you lose the "premium" positioning
- **Verdict:** Only if CMF is fully automated

### Option B: Hybrid (Keep $250/mo as "Concierge" tier)
```
$25/week  → Self-service, automated pipeline
$50/week  → Self-service premium, more volume
$250/mo   → White-glove, strategy calls, priority queue
$4/user   → CBCS credits (all tiers)
```
- **Pro:** Captures both "I just want content" AND "I want a partner"
- **Con:** More complexity to manage
- **Verdict:** ✅ **Recommended.** The $250 tier becomes upsell for coaches who outgrow self-service

### Option C: Your Proposal (Pure Weekly)
```
$25/week  → Basic self-service
$50/week  → Premium self-service  
$4/user   → CBCS credits
```
- **Pro:** Maximum growth velocity, lowest barrier, simplest positioning
- **Con:** Revenue per coach is lower, need volume faster
- **Verdict:** Best if priority is adoption speed over short-term revenue

---

## Recommended Updated Revenue Roadmap

| Phase | Strategy | Target | Revenue |
|---|---|---|---|
| **Phase 1** (Month 1-3) | Push $25/week hard. Get 40 coaches. | 40 coaches × $100/mo | $4,000/mo |
| **Phase 2** (Month 3-6) | Upsell 15→ $50/week. Deploy CBCS. | 25@$100 + 15@$200 + CBCS | $8,250/mo |
| **Phase 3** (Month 6+) | Scale CBCS. 50 coaches, 100 users each. | Content + 5,000 CBCS users | $20,000+/mo |

> [!NOTE]
> **Key metric to track:** CBCS conversion rate. If >40% of weekly coaches activate CBCS within 60 days, this model is strictly superior to the retainer model. The $4/user backend is where the real money is — weekly pricing is just the faster highway to get there.

---

## Update to Business Plan Needed?

If you go forward with this, the following sections of the business plan need revision:

1. **Section 5 (Strategic Offers)** — Replace Phase 1-2 pricing tiers with weekly model
2. **Section 6 (Financial Roadmap)** — Recalculate milestones with new unit economics  
3. **Section 1 (Executive Summary)** — Update the "Mechanism" to reflect self-service entry
4. **Section 7 (Operational Plan)** — Adjust batch schedule for higher content volume

Want me to update the business plan with the new pricing model?
