# CCP Research Intelligence Stack — Strategic Query Plan

**Problem:** Our current research skills (DEEP V3.1, FRESH V2.1) use generic queries with no pre-filtering, no image sourcing, and no Reddit/YouTube integration. Result: high noise, wasted API calls, unusable images, double work for agents cleaning junk data.

**Goal:** Every API call returns data worth keeping. Zero junk. Zero wasted requests.

**Philosophy:** Evergreen pain patterns, intent mapping, and high-quality contextual synthesis — NOT short-term viral trends.

---

## The 4 Research APIs and Their Exact Purpose

| API | Purpose | What It Replaces | Cost Sensitivity |
|---|---|---|---|
| **Reddit API** | Conversation mining, objection extraction, tribal language capture, trend validation via recurring discussions | Nothing (NEW) | LOW — free tier generous |
| **YouTube Data API** | Niche audience sentiment, comment analysis, content format intelligence, trend validation via recurring topics | Nothing (NEW) | LOW — quota-based |
| **Serper.dev** | Google Search (organic, PAA, autocomplete, News, Images) with geo/date filters. Intent mining + IRL image sourcing | Generic web_search + Outscraper + Google Trends | HIGH — every query must count |
| **Firecrawl** | Structured depth extraction from authoritative sources | Already integrated | MEDIUM — per-page billing |

> [!IMPORTANT]
> **Each API is NOT a search engine.** Each API answers ONE specific type of question.
> Using the wrong API for the wrong question = wasted money + junk data.

---

## The 4 Research Layers (What We Query, in Order)

### Layer 1: AUDIENCE VOICE MINING (Reddit API) — "What are real people ACTUALLY saying?"

**Purpose:** Reddit is the largest corpus of raw, unfiltered human language about pain, desire, confusion, and breakthroughs. Also serves as **trend validation** — recurring discussions across subreddits signal sustained audience interest.

**Subreddits to Mine (Holistic + Mindset Coaching):**
```python
PRIMARY_SUBREDDITS = [
    "r/selfimprovement",
    "r/DecidingToBeBetter",
    "r/getdisciplined",
    "r/Mindfulness",
    "r/meditation",
    "r/socialanxiety",
    "r/confidence",
    "r/productivity",
    "r/mentalhealth",
    "r/BreakUps",          # emotional processing
    "r/relationships",     # relational dynamics
    "r/AskWomen",          # if coach targets women
    "r/AskMen",            # if coach targets men
]

# Per-coach custom additions from tribe_profile.json
COACH_SUBREDDITS = tribe_profile["reddit_communities"]  # populated during onboarding
```

**Query Strategy (3 Types):**

| Query Type | Reddit Endpoint | What It Returns | Signal |
|---|---|---|---|
| **Hot Pain** | `/r/{sub}/search?q={theme}&sort=relevance&t=month` | Top threads about the theme from last 30 days | Exact language of frustration, confusion, desire |
| **Top Confessions** | `/r/{sub}/search?q={theme}&sort=top&t=year` | Highest-upvoted threads of all time | Universal truths the tribe resonates with deepest |
| **Comment Gold** | `/r/{sub}/comments/{thread_id}` (top 20 comments) | Raw emotional responses | Tribal slang, metaphors, objections, breakthroughs |

**Pre-Filter Rules:**
- Skip threads with <10 upvotes (low signal)
- Skip threads with <5 comments (no engagement = no tribe energy)
- Skip `[removed]` or `[deleted]` posts
- Extract ONLY: post title, post body (first 500 chars), top 5 comments, upvote count, comment count
- **Never extract usernames** — privacy first

**Output:** `reddit_voice_mining.json` — array of pain statements, desire statements, objections, and exact tribal language

**Cost:** Free tier allows 60 requests/min. Budget: ~20 requests per research cycle.

---

### Layer 2: NICHE PULSE (YouTube Data API) — "What content is PERFORMING right now?"

**Purpose:** YouTube comments reveal what the audience FEELS about content they just consumed. Recurring topics across creators = **trend validation** (replaces Google Trends for our niche). Comment analysis reveals what the audience WISHES the creator had covered.

**Query Strategy:**

| Query Type | API Call | What It Returns | Signal |
|---|---|---|---|
| **Trending Content** | `search.list(q="{theme}", order="viewCount", publishedAfter="{30_days_ago}")` | Most-viewed recent videos about the theme | What angles are getting attention right now |
| **Rising Creators** | `search.list(q="{theme}", order="date", publishedAfter="{7_days_ago}")` | Brand new videos (last 7 days) | Early signals before they trend |
| **Comment Sentiment** | `commentThreads.list(videoId="{top_video_id}", maxResults=50, order="relevance")` | Top 50 comments on trending videos | Raw audience reaction to competing content |

**Pre-Filter Rules:**
- Only videos with >1,000 views (below this = no signal)
- Only videos <20 minutes (longer = different content category)
- Only English/French (match coach audience language)
- Extract ONLY: video title, channel name, view count, publish date, top 10 comments
- **Skip** videos from mega-channels (>5M subs) — their audience is too broad to be tribal

**Output:** `youtube_pulse.json` — trending angles, performing formats, audience sentiment quotes

**Cost:** YouTube Data API quota = 10,000 units/day (free). Budget: ~30 requests per cycle = ~3,100 units.

---

### Layer 3: INTENT + IMAGES (Serper.dev) — "What do people SEARCH for, and what do they SEE?"

**Purpose:** Serper.dev has four critical roles:
1. **PAA Intent Signals** — People Also Ask reveals the exact questions people type
2. **Autocomplete Suggestions** — reveals how people START typing about a topic
3. **News Velocity** — surge in news articles = trending topic (replaces Google Trends)
4. **High-Quality Image Sourcing** — IRL authentic images with geo/date filters

> [!CAUTION]
> This is the MOST EXPENSIVE API. Every query must be laser-targeted. No broad searches.

**Query Strategy:**

#### A. Intent Mining (PAA + Autocomplete + News)
```
Serper.dev endpoint: /search
params:
  q: "{theme} + {tribe_pain_point}"     # e.g., "emotional eating shame recovery"
  gl: "{coach_audience_country}"
  hl: "{language}"
  num: 10

Extract:
  → peopleAlsoAsk — the exact questions people ask
  → relatedSearches — what they search next
  → organic[0:3].snippet — top 3 result summaries
  → news — recent articles with date (trend velocity signal)
  → autocompleteSuggestions — how people START typing
```

**Pre-Filter Rules for PAA:**
- Keep ONLY questions that contain emotional/action language ("how to", "why do I", "is it normal to", "what happens when")
- Discard informational-only questions ("what is", "define", "history of") — too broad
- Cross-reference PAA questions against Reddit pain statements (Layer 1) — overlapping questions = HIGHEST SIGNAL

#### B. Image Sourcing — Two Lanes

Image sourcing is split by PURPOSE:

**Lane 1: Cultural Recognition (Serper.dev `/images` endpoint)**
For finding recognizable cultural objects and moments the tribe has emotional attachment to.
```
Serper.dev endpoint: /images
params:
  q: "{specific_cultural_reference}"    # Name the SPECIFIC thing
  gl: "{coach_audience_country}"
  num: 10

Examples:
  ✅ "Atomic Habits book cover James Clear"      → tribe recognizes instantly
  ✅ "Huberman Lab podcast studio"               → audience knows this face
  ✅ "journaling morning coffee aesthetic 2024"   → trending visual the tribe shares
  ❌ "man staring at empty notebook thinking stuck" → mood description, use Pexels
```

**Lane 2: Lifestyle Scenes (Pexels / Unsplash / Pixabay / GIPHY)**
For clean, curated, watermark-free lifestyle photography and reactions.

| API | Best For | Query Style |
|---|---|---|
| **Pexels** | Lifestyle scenes, emotions, human connection | `"woman overwhelmed kitchen morning"` — curated, no watermarks |
| **Unsplash** | Premium editorial/hero images, cover photos | `"solitary walk nature contemplation"` — artistic, semi-pro quality |
| **Pixabay** | Volume, variety, illustrations + vectors | `"meditation workspace calm"` — broadest library, mixed media |
| **GIPHY** | Reaction GIFs, relatable emotional moments | `"overwhelmed gif"`, `"breakthrough celebration"` — social native |

> [!IMPORTANT]
> **Two Rules:**
> - **Serper.dev:** Name the SPECIFIC thing. The tribe must RECOGNIZE it.
> - **Pexels/Unsplash/Pixabay:** Describe the MOOD/SCENE. Curated sources handle lifestyle better than Google.
> - **GIPHY:** Emotion keyword + "gif". Used for carousels, social, Telegram bot responses.

**Image Quality Checklist (all lanes):**
- [ ] Resolution ≥ 800x600 (reject thumbnails)
- [ ] No watermarks (Pexels/Unsplash/Pixabay are clean; Serper.dev results need source URL validation)
- [ ] Not a text overlay / infographic (reject if image is primarily text)
- [ ] Depicts a PERSON or real-world SCENE (reject abstract/graphic/logos)
- [ ] Aspect ratio between 3:4 and 16:9 (reject extreme ratios)

**Cost:** Serper.dev images = PAID (part of the 15 queries/cycle budget). Pexels/Unsplash/Pixabay = FREE tier. GIPHY = FREE tier.

---

### Layer 4: DEEP EXTRACTION (Firecrawl) — "Give me the FULL source"

**Purpose:** Layers 1-3 give us signals, language, and visuals. Layer 4 gives us the SUBSTANCE — full articles, studies, expert interviews from authoritative sources that become the backbone of the content script.

**When to Use Firecrawl:**
- ONLY on URLs surfaced by Serper.dev or YouTube results that scored HIGH signal
- NEVER as a first-pass search tool (too expensive for discovery)
- Used to extract: full article text, author credentials, publication date, data tables

**Query Strategy:**
```
NOT: firecrawl_search("mindset coaching techniques")  ← waste of money
YES: firecrawl_scrape("https://specific-high-signal-url.com/article")  ← targeted extraction
```

**Pre-Filter Rule:** Only scrape URLs that passed the signal test in Layers 1-3. If a URL was found via Reddit (high-upvote thread linking to an article) or Serper.dev (top 3 organic result), it qualifies for deep extraction. Random URLs do not.

**Cost:** Firecrawl = per-page billing. Budget: **max 8-12 scrapes per research cycle.** Only the highest-signal URLs.

---

## The Research Cascade (Full Flow)

```
┌─────────────────────────────────────────┐
│ Layer 1: Reddit API (FREE)              │ ← "What are people SAYING?"
│   → Pain/desire language                │
│   → Tribal vocabulary                   │
│   → Objections & skepticism             │
│   → Trend validation (recurring topics) │
└──────────┬──────────────────────────────┘
           │ pain terms + validated topics feed into ↓
┌──────────▼──────────────────────────────┐
│ Layer 2: YouTube Data API (FREE)        │ ← "What content is WORKING?"
│   → Performing angles & formats         │
│   → Comment sentiment                   │
│   → Competitive intelligence            │
│   → Trend validation (recurring videos) │
└──────────┬──────────────────────────────┘
           │ validated angles feed into ↓
┌──────────▼──────────────────────────────┐
│ Layer 3: Serper.dev (PAID — precise)    │ ← "What do people SEARCH for + need to SEE?"
│   → PAA intent signals                  │
│   → Autocomplete suggestions            │
│   → News velocity (trend signal)        │
│   → IRL authentic images                │
│   → Only after Reddit/YT validate       │
└──────────┬──────────────────────────────┘
           │ high-signal URLs feed into ↓
┌──────────▼──────────────────────────────┐
│ Layer 4: Firecrawl (PAID — deep)        │ ← "Give me the FULL source"
│   → Full article text                   │
│   → Expert quotes, data tables          │
│   → Only URLs from Layers 1-3           │
└─────────────────────────────────────────┘
```

> [!IMPORTANT]
> **The cascade is directional. Each layer REDUCES the search space for the next.**
> - Layer 1 tells you WHAT LANGUAGE + validates trends (tribal voice + recurring discussions)
> - Layer 2 tells you WHAT WORKS + validates trends (proven angles + recurring topics)
> - Layer 3 tells you WHAT TO TARGET (precise queries + images + News velocity) — using insights from 1-2
> - Layer 4 tells you THE SUBSTANCE (deep extraction) — only for URLs from Layer 3
>
> **You never arrive at Serper.dev or Firecrawl without first passing through the free layers.**

**Trend Validation Without Google Trends:** Trend signals come from: (1) **Serper.dev News velocity** — a surge in recent news articles = trending. (2) **Reddit + YouTube recurring discussions** — the same topic appearing across subreddits and creator videos within 2-4 weeks = sustained audience interest. More reliable for coaching than Google Trends (which skews toward viral/pop culture).

---

## Cost Budget Per Research Cycle

| Layer | API | Requests | Cost |
|---|---|---|---|
| 1 | Reddit | ~20 | Free |
| 2 | YouTube | ~30 | Free (quota) |
| 3 | Serper.dev | ~15 | ~$0.15 |
| 4 | Firecrawl | ~10 | ~$0.50 |
| **Total** | | **~75 requests** | **~$0.65 per research cycle** |

At 24 coaches × 4 research cycles/month = 96 cycles = **~$62/month total research cost.**
