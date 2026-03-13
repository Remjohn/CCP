# CMF V13 Workflow Guide

## Goal: 40 Videos/Week = $4,000/Month

| Metric | Target |
|--------|--------|
| Daily | 8 videos |
| Weekly | 40 videos |
| Monthly | 160 videos |
| Value | $25/video |
| **Monthly Revenue** | **$4,000** |

---

## Stage 1: Frame Discovery & Arc Selection

### Step 1: Read the Transcript
Read the entire transcript and ask: **"What is the emotional journey?"**

### Step 2: Identify the Frame
Use this decision tree:

```
Is this a CLIENT telling their story? 
├─ YES → Use THE WITNESS HUNTER
└─ NO → Is the COACH speaking solo?
         ├─ YES → What's the emotional journey?
         │        ├─ "Lost → Found answer" → Core Transformation
         │        ├─ "Couldn't breathe → Clarity" → Breakthrough
         │        ├─ "Looking back, I understand" → Quiet Reflection
         │        ├─ "Everyone gets this wrong" → Confrontation
         │        ├─ "You think X but Y" (humor) → Comedic Reframe
         │        ├─ "Empty → Grace arrived" → Divine Spark
         │        ├─ "Something was calling me" → Call to Adventure
         │        ├─ "Knocked down → Got back up" → Rally
         │        ├─ "Time was running out" → Ticking Clock
         │        ├─ "Left, learned, returned" → Sacred Return
         │        ├─ "Thought I was alone → Found my people" → Shared Struggle
         │        └─ "This is what happens if you don't listen" → Warning
         └─ NO → It's an INTERVIEW → Apply above logic to content
```

---

## The 13 Arc Hunters — Complete Reference

### 🎯 THE WITNESS HUNTER (Testimonial-Specific)

| Property | Value |
|----------|-------|
| **Best For** | Client testimonials, transformation stories |
| **Emotional Journey** | Hook → Problem → Mechanism → Proof → Close |
| **Critical Rules** | Coach in HOOK and CLOSE, Numbers in PROOF |

**Use When:** Client is telling their experience with the coach.

---

### 12 Sonic Arc Hunters

| # | Arc | Emotional Journey | Use When Content Feels Like... |
|---|-----|-------------------|-------------------------------|
| 1 | **Core Transformation** | Intrigue → Vulnerability → Realization → Empowerment | "I was lost, then I found the answer" |
| 2 | **Breakthrough** | Anxiety → Struggle → Epiphany → Empowerment | "I couldn't breathe, then clarity came" |
| 3 | **Quiet Reflection** | Nostalgia → Confusion → Acceptance → Peace | "Looking back, I now understand" |
| 4 | **Confrontation** | Frustration → Debate → Clarity → Confidence | "Everyone gets this wrong, here's truth" |
| 5 | **Comedic Reframe** | Normalcy → Absurd → Ironic Laugh → Relief | "You think X but actually Y" (with humor) |
| 6 | **Divine Spark** | Emptiness → Surrender → Grace → Purpose | "I was empty, then grace arrived" |
| 7 | **Call to Adventure** | Restlessness → Contemplation → Spark → First Step | "Something was calling me" |
| 8 | **Rally** | Setback → Frustration → Focus → Action | "I got knocked down, but got back up" |
| 9 | **Ticking Clock** | Stagnation → Urgency → Decision → Momentum | "Time was running out" |
| 10 | **Sacred Return** | Departure → Trials → Return → Gift | "I left, learned, and returned with gifts" |
| 11 | **Shared Struggle** | Isolation → Recognition → Unity → Power | "I thought I was alone, then found my people" |
| 12 | **Warning** | Normalcy → Signs → Crisis → Lesson | "This is what happens if you don't listen" |

---

## Arc Hunter Agent Files

**Location:** `🇫🇷 Conscious Movie Factory/agents/arc_hunters/`

| Arc | English Agent | French Agent |
|-----|---------------|--------------|
| Witness | `🔎 THE WITNESS HUNTER.md` | `🇫🇷 🔎 THE WITNESS HUNTER.md` |
| Core Transformation | `🔎 THE CORE TRANSFORMATION HUNTER.md` | `🇫🇷 🔎 THE CORE TRANSFORMATION HUNTER.md` |
| Breakthrough | `🔎 THE BREAKTHROUGH HUNTER.md` | `🇫🇷 🔎 THE BREAKTHROUGH HUNTER.md` |
| Quiet Reflection | `🔎 THE QUIET REFLECTION HUNTER.md` | `🇫🇷 🔎 THE QUIET REFLECTION HUNTER.md` |
| Confrontation | `🔎 THE CONFRONTATION HUNTER.md` | `🇫🇷 🔎 THE CONFRONTATION HUNTER.md` |
| Comedic Reframe | `🔎 THE COMEDIC REFRAME HUNTER.md` | `🇫🇷 🔎 THE COMEDIC REFRAME HUNTER.md` |
| Divine Spark | `🔎 THE DIVINE SPARK HUNTER.md` | `🇫🇷 🔎 THE DIVINE SPARK HUNTER.md` |
| Call to Adventure | `🔎 THE CALL TO ADVENTURE HUNTER.md` | `🇫🇷 🔎 THE CALL TO ADVENTURE HUNTER.md` |
| Rally | `🔎 THE RALLY HUNTER.md` | `🇫🇷 🔎 THE RALLY HUNTER.md` |
| Ticking Clock | `🔎 THE TICKING CLOCK HUNTER.md` | `🇫🇷 🔎 THE TICKING CLOCK HUNTER.md` |
| Sacred Return | `🔎 THE SACRED RETURN HUNTER.md` | `🇫🇷 🔎 THE SACRED RETURN HUNTER.md` |
| Shared Struggle | `🔎 THE SHARED STRUGGLE HUNTER.md` | `🇫🇷 🔎 THE SHARED STRUGGLE HUNTER.md` |
| Warning | `🔎 THE WARNING HUNTER.md` | `🇫🇷 🔎 THE WARNING HUNTER.md` |

**Master Guide:** `🎯 ARC SELECTION GUIDE.md`

---

## Stage 2: Script Extraction

1. Open the selected Arc Hunter agent file
2. Follow the **Chain of Thought Template** in the agent
3. Extract quotes per cluster (each arc has specific phases)
4. Calculate viral scores: `(SURPRISE × EMOTION × SPECIFICITY) / 100`
5. Output `final_script.json` in Arc Hunter format

---

## Stage 3: Asset Generation

1. **Generate Storyboard** → Virtual Director agent
2. **Run on RunningHub** (manual) → T2I, I2V, Upscale
3. **Cut A-Roll Scenes** → Composition page in Streamlit

---

## Stage 4: Music & Assembly

1. **Generate Lyrics** → Sonic Scribe agent
2. **Create on Suno.ai** (manual)
3. **Assemble** → Import all assets, follow storyboard

---

## Quick Commands

```powershell
cd "D:\Work\The Conscious Movie Factory December\CMF labo\director_console"
python -m streamlit run app.py
```
