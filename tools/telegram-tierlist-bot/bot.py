"""
bot.py — Telegram Tier List & Rating Idea Bot

CLI entry point that generates tier list / rating ideas
and sends them to coaches via Telegram.

Usage:
    python bot.py --coach "Coach Adele"                  # Generate & send
    python bot.py --coach "Coach Adele" --dry-run        # Preview only
    python bot.py --coach "Coach Adele" --test           # Test Telegram connection
    python bot.py --coach "Coach Adele" --week 2026-W08  # Specific week
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

from generator import generate_ideas, save_ideas, resolve_week_id
from formatter import format_ideas_message, format_test_message, format_selection_confirmation


# ── Constants ────────────────────────────────────────────────
PRODUCTION_DIR = Path(__file__).resolve().parent.parent.parent / "production"
DEFAULT_ARCHETYPE_DIR = Path(__file__).resolve().parent.parent.parent / "ccf-26" / "intelligence" / "archetype_prompts"


def find_coach_dir(coach_name: str) -> Path:
    """Find the coach's project directory under production/."""
    if not PRODUCTION_DIR.exists():
        raise FileNotFoundError(f"Production directory not found: {PRODUCTION_DIR}")

    # Try exact match first
    coach_dir = PRODUCTION_DIR / coach_name
    if coach_dir.exists():
        return coach_dir

    # Try case-insensitive partial match
    for d in PRODUCTION_DIR.iterdir():
        if d.is_dir() and coach_name.lower() in d.name.lower():
            return d

    raise FileNotFoundError(
        f"Coach directory not found for '{coach_name}'. "
        f"Available: {[d.name for d in PRODUCTION_DIR.iterdir() if d.is_dir()]}"
    )


def load_coach_config(coach_dir: Path) -> dict:
    """Load the coach's telegram config file."""
    config_file = coach_dir / "coach_telegram_config.yaml"
    if not config_file.exists():
        raise FileNotFoundError(
            f"No coach_telegram_config.yaml in {coach_dir}. "
            f"Copy from ccf-26/templates/coach_telegram_config.yaml"
        )
    return yaml.safe_load(config_file.read_text(encoding="utf-8"))


async def send_telegram_message(chat_id: str, text: str, bot_token: str) -> bool:
    """Send a message via the Telegram Bot API."""
    import httpx

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": None,  # Plain text — MarkdownV2 is too fragile
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            return True
        else:
            print(f"❌ Telegram API error: {response.status_code} — {response.text}")
            return False


async def run_test(config: dict):
    """Send a test message to verify Telegram connection."""
    chat_id = config.get("telegram", {}).get("chat_id", "")
    token_env = config.get("telegram", {}).get("bot_token_env", "TELEGRAM_BOT_TOKEN")
    bot_token = os.environ.get(token_env, "")
    coach_name = config.get("coach_name", "")

    if not chat_id or not bot_token:
        print("❌ Missing telegram.chat_id or bot token.")
        print(f"   chat_id: {'set' if chat_id else 'MISSING'}")
        print(f"   bot_token ({token_env}): {'set' if bot_token else 'MISSING'}")
        return False

    msg = format_test_message(coach_name)
    print(f"📤 Sending test message to chat_id={chat_id}...")
    success = await send_telegram_message(chat_id, msg, bot_token)
    if success:
        print("✅ Test message sent successfully!")
    return success


async def run_generate_and_send(config: dict, coach_dir: Path, week_id: str = None, dry_run: bool = False):
    """Generate ideas and send them to the coach."""
    coach_name = config.get("coach_name", "Unknown")
    wid = week_id or resolve_week_id()

    print(f"🧠 Generating ideas for {coach_name} — Week {wid}")
    print(f"   Format: {config.get('content', {}).get('format', 'mixed')}")
    print(f"   Archetypes: {config.get('content', {}).get('preferred_archetypes', [])}")
    print()

    # Find archetype directory
    archetype_dir = str(DEFAULT_ARCHETYPE_DIR)
    custom_arch = config.get("paths", {}).get("archetype_prompts_dir")
    if custom_arch:
        custom_path = (coach_dir / custom_arch).resolve()
        if custom_path.exists():
            archetype_dir = str(custom_path)

    # Generate ideas
    try:
        ideas = await generate_ideas(
            coach_config=config,
            coach_project_dir=str(coach_dir),
            archetype_base_dir=archetype_dir,
            week_id=wid,
            dry_run=dry_run,
        )
    except FileNotFoundError as e:
        print(f"⚠️  {e}")
        print("   Make sure ccf-weekly has been run first to generate themes.")
        return False
    except Exception as e:
        print(f"❌ Error generating ideas: {e}")
        return False

    # Save ideas
    output_file = save_ideas(ideas, str(coach_dir), wid)
    print(f"💾 Ideas saved to: {output_file}")

    # Format message
    msg = format_ideas_message(ideas, wid, coach_name)
    print()
    print("=" * 50)
    print("📝 MESSAGE PREVIEW:")
    print("=" * 50)
    print(msg)
    print("=" * 50)

    if dry_run:
        print("\n🏃 Dry run — message NOT sent to Telegram.")
        return True

    # Send via Telegram
    chat_id = config.get("telegram", {}).get("chat_id", "")
    token_env = config.get("telegram", {}).get("bot_token_env", "TELEGRAM_BOT_TOKEN")
    bot_token = os.environ.get(token_env, "")

    if not chat_id or not bot_token:
        print("⚠️  Telegram not configured — ideas saved but not sent.")
        print(f"   Set telegram.chat_id in config and {token_env} in .env")
        return True

    print(f"\n📤 Sending to Telegram (chat_id={chat_id})...")
    success = await send_telegram_message(chat_id, msg, bot_token)
    if success:
        print("✅ Ideas sent to Telegram!")
    return success


def main():
    parser = argparse.ArgumentParser(
        description="Telegram Tier List & Rating Idea Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bot.py --coach "Coach Adele"                  # Generate & send
  python bot.py --coach "Coach Adele" --dry-run        # Preview only
  python bot.py --coach "Coach Adele" --test           # Test connection
  python bot.py --coach "Coach Adele" --week 2026-W08  # Specific week
        """,
    )
    parser.add_argument("--coach", required=True, help="Coach name (matches production/ folder)")
    parser.add_argument("--dry-run", action="store_true", help="Generate ideas without sending to Telegram")
    parser.add_argument("--test", action="store_true", help="Send a test message to verify Telegram connection")
    parser.add_argument("--week", default=None, help="ISO week ID (e.g., 2026-W08). Defaults to current week.")

    args = parser.parse_args()

    # Load .env
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)

    # Find coach directory & config
    try:
        coach_dir = find_coach_dir(args.coach)
        config = load_coach_config(coach_dir)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)

    print(f"📋 Loaded config for: {config.get('coach_name', args.coach)}")
    print(f"📂 Coach directory: {coach_dir}")
    print()

    # Run
    if args.test:
        success = asyncio.run(run_test(config))
    else:
        success = asyncio.run(run_generate_and_send(config, coach_dir, args.week, args.dry_run))

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
