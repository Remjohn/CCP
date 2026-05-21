import sys
import re
from src.ccp.models.validation_gate_models import SeasonMandate

forge_draft = (
    "Stop waiting for the perfect moment. That moment died while you were "
    "scrolling through your phone looking for motivation. Here is the hard "
    "truth about discipline: action precedes clarity. You will never feel "
    "ready. The forge does not care about your feelings. It cares about your "
    "commitment. Step one: write down the one thing you have been avoiding. "
    "Step two: do it before noon tomorrow. No excuses. No negotiation. "
    "Build the habit of doing what scares you. Execute daily. Commit fully. "
    "The grind is the teacher. Work through the resistance."
)

mirror_draft = (
    "I remember the afternoon I realized I had been lying to myself for "
    "years. Not a dramatic lie — a quiet one. The kind you tell yourself "
    "when you look in the mirror and pretend everything is fine. I had to "
    "sit with that discomfort. Journal about it. Reflect on every choice "
    "that led me there. Self-examination is not comfortable. But it is "
    "the only path to knowing who you actually are beneath the story you "
    "tell the world. Look within. Remember who you were before the mask. "
    "Introspect deeply before you take another step forward."
)

season_keywords = {
    SeasonMandate.DECONSTRUCTION: [
        "challenge", "false belief", "question", "dismantle",
        "expose", "uncomfortable truth", "break down", "myth",
    ],
    SeasonMandate.THE_FORGE: [
        "action", "discipline", "hard step", "forge",
        "build", "execute", "commit", "grind", "work",
    ],
    SeasonMandate.THE_MIRROR: [
        "introspect", "reflect", "story", "mirror",
        "look within", "journal", "remember", "self",
    ],
    SeasonMandate.THE_TRIBE: [
        "community", "we", "together", "tribe",
        "collective", "share", "belong", "us",
    ],
}

def has_word(kw: str, text: str) -> bool:
    pattern = r"\b" + re.escape(kw) + r"\b"
    return bool(re.search(pattern, text, re.IGNORECASE))

print("--- With word boundaries: FORGE DRAFT under THE_FORGE ---")
active_keywords = season_keywords[SeasonMandate.THE_FORGE]
active_hits = sum(1 for kw in active_keywords if has_word(kw, forge_draft))
active_coverage = active_hits / len(active_keywords)
print(f"Active hits: {active_hits}/{len(active_keywords)} ({active_coverage:.4f})")

wrong_season_hits = 0
for other_season, keywords in season_keywords.items():
    if other_season != SeasonMandate.THE_FORGE:
        for kw in keywords:
            if has_word(kw, forge_draft):
                print(f"Matched wrong keyword: {kw}")
                wrong_season_hits += 1

contamination_penalty = min(wrong_season_hits * 0.1, 0.5)
compliance = min(1.0, max(0.0, active_coverage - contamination_penalty))
print(f"Final compliance: {compliance:.4f}")


print("\n--- With word boundaries: MIRROR DRAFT under THE_MIRROR ---")
active_keywords = season_keywords[SeasonMandate.THE_MIRROR]
active_hits = sum(1 for kw in active_keywords if has_word(kw, mirror_draft))
active_coverage = active_hits / len(active_keywords)
print(f"Active hits: {active_hits}/{len(active_keywords)} ({active_coverage:.4f})")

wrong_season_hits = 0
for other_season, keywords in season_keywords.items():
    if other_season != SeasonMandate.THE_MIRROR:
        for kw in keywords:
            if has_word(kw, mirror_draft):
                print(f"Matched wrong keyword: {kw}")
                wrong_season_hits += 1

contamination_penalty = min(wrong_season_hits * 0.1, 0.5)
compliance = min(1.0, max(0.0, active_coverage - contamination_penalty))
print(f"Final compliance: {compliance:.4f}")
