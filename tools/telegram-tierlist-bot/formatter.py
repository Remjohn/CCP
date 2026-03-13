"""
formatter.py — Telegram Message Formatter

Takes a list of generated ideas and formats them into
a visually appealing Telegram message.
"""


# ── Archetype emoji mapping ──────────────────────────────────
ARCHETYPE_EMOJI = {
    "authority":     "👑",
    "controversial": "⚡",
    "roast":         "🔥",
    "relatable":     "💬",
    "red-flag":      "🚩",
}

FORMAT_EMOJI = {
    "tierlist": "📊",
    "rating":   "⭐",
}


def format_ideas_message(ideas: list[dict], week_id: str, coach_name: str = "") -> str:
    """
    Format a list of ideas into a Telegram-friendly message.

    Args:
        ideas: List of idea dicts from generator.py
        week_id: ISO week string (e.g., '2026-W08')
        coach_name: Coach's display name

    Returns:
        Formatted string ready for Telegram (MarkdownV2-compatible plain text)
    """
    greeting = f"Hey {coach_name} 👋\n" if coach_name else ""

    header = (
        f"{greeting}"
        f"📊 Week {week_id} — Tier List & Rating Ideas\n"
        f"{'━' * 38}\n"
    )

    idea_blocks = []
    for i, idea in enumerate(ideas, 1):
        fmt = idea.get("format", "tierlist")
        archetype = idea.get("archetype", "authority")
        title = idea.get("title", f"Idea #{i}")
        description = idea.get("description", "")
        duration = idea.get("estimated_duration", "6-8 min")

        fmt_label = fmt.upper().replace("TIERLIST", "TIER LIST")
        fmt_emoji = FORMAT_EMOJI.get(fmt, "📊")
        arch_emoji = ARCHETYPE_EMOJI.get(archetype, "✨")
        arch_label = archetype.replace("-", " ").title()

        block = (
            f"{'━' * 38}\n"
            f"{fmt_emoji} IDEA {i} — {fmt_label} ({arch_label})\n"
            f"{'━' * 38}\n"
            f"\n"
            f"🎬 \"{title}\"\n"
            f"\n"
            f"💡 {description}\n"
            f"\n"
            f"{arch_emoji} Archetype: {arch_label}\n"
            f"⏱️ Duration: {duration}\n"
        )
        idea_blocks.append(block)

    # Reply buttons hint
    num_ideas = len(ideas)
    reply_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    reply_options = ", ".join(reply_emojis[:num_ideas])

    footer = (
        f"\n{'━' * 38}\n"
        f"\n"
        f"Reply with {reply_options} to pick an idea\n"
        f"for this week's recording guide.\n"
        f"\n"
        f"Or reply 🔄 to regenerate new ideas."
    )

    return header + "\n".join(idea_blocks) + footer


def format_test_message(coach_name: str = "") -> str:
    """Format a test message to verify Telegram connection."""
    return (
        f"🧪 Test Message — Tier List Bot\n"
        f"{'━' * 38}\n"
        f"\n"
        f"✅ Connection working!\n"
        f"{'━' * 38}\n"
        f"Coach: {coach_name or 'Unknown'}\n"
        f"Bot is ready to send weekly ideas.\n"
        f"\n"
        f"Run with --dry-run to preview ideas,\n"
        f"or wait for the scheduled delivery."
    )


def format_selection_confirmation(idea: dict, idea_number: int) -> str:
    """Format a confirmation message when coach selects an idea."""
    title = idea.get("title", f"Idea #{idea_number}")
    archetype = idea.get("archetype", "authority")
    fmt = idea.get("format", "tierlist").upper().replace("TIERLIST", "TIER LIST")
    arch_emoji = ARCHETYPE_EMOJI.get(archetype, "✨")

    return (
        f"✅ Great choice!\n"
        f"\n"
        f"{arch_emoji} Selected: \"{title}\"\n"
        f"📊 Format: {fmt}\n"
        f"\n"
        f"I'll save this as the pick for this week.\n"
        f"Your recording guide will reference this idea."
    )
