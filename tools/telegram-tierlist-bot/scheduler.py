"""
scheduler.py — Daily Scheduler for Tier List Bot

Checks all coach configs and triggers idea delivery
when today matches the coach's configured delivery day.

Usage:
    python scheduler.py              # One-shot check (run via cron/task scheduler)
    python scheduler.py --daemon     # Keep running, check daily
    python scheduler.py --list       # List all configured coaches
"""

import argparse
import asyncio
import os
import subprocess
import sys
import time
from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml
from dotenv import load_dotenv


# ── Constants ────────────────────────────────────────────────
PRODUCTION_DIR = Path(__file__).resolve().parent.parent.parent / "production"
BOT_SCRIPT = Path(__file__).resolve().parent / "bot.py"


def discover_coaches() -> list[dict]:
    """Find all coach directories with telegram configs."""
    coaches = []
    if not PRODUCTION_DIR.exists():
        return coaches

    for coach_dir in PRODUCTION_DIR.iterdir():
        if not coach_dir.is_dir():
            continue

        config_file = coach_dir / "coach_telegram_config.yaml"
        if not config_file.exists():
            continue

        try:
            config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
            coaches.append({
                "name": config.get("coach_name", coach_dir.name),
                "dir": coach_dir,
                "config": config,
            })
        except Exception as e:
            print(f"⚠️  Error reading config in {coach_dir.name}: {e}")

    return coaches


def should_send_today(config: dict) -> bool:
    """Check if today is the configured delivery day for this coach."""
    delivery = config.get("delivery", {})
    send_day = delivery.get("day", "thursday").lower()
    tz_name = delivery.get("timezone", "UTC")

    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = ZoneInfo("UTC")

    today = datetime.now(tz)
    today_day = today.strftime("%A").lower()

    return today_day == send_day


def is_within_delivery_window(config: dict) -> bool:
    """Check if current time is within 30 minutes of configured delivery time."""
    delivery = config.get("delivery", {})
    send_time = delivery.get("time", "09:00")
    tz_name = delivery.get("timezone", "UTC")

    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = ZoneInfo("UTC")

    now = datetime.now(tz)
    target_hour, target_minute = map(int, send_time.split(":"))

    # Check if we're within a 30-minute window of the target time
    now_minutes = now.hour * 60 + now.minute
    target_minutes = target_hour * 60 + target_minute
    diff = abs(now_minutes - target_minutes)

    return diff <= 30


def has_sent_this_week(coach_dir: Path) -> bool:
    """Check if ideas have already been sent this week."""
    from generator import resolve_week_id
    wid = resolve_week_id()
    ideas_file = coach_dir / "intelligence" / "weekly" / wid / "tierlist_rating_ideas.json"
    return ideas_file.exists()


def run_bot_for_coach(coach_name: str, coach_dir: Path):
    """Run bot.py as a subprocess for a specific coach."""
    cmd = [sys.executable, str(BOT_SCRIPT), "--coach", coach_name]
    print(f"  🚀 Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            cwd=str(BOT_SCRIPT.parent),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            print(f"  ✅ Done for {coach_name}")
        else:
            print(f"  ❌ Failed for {coach_name}:")
            print(f"     {result.stderr[-300:]}" if result.stderr else "     (no error output)")
    except subprocess.TimeoutExpired:
        print(f"  ⏰ Timeout for {coach_name} (120s)")


def run_check():
    """One-shot: check all coaches and send if today is their day."""
    coaches = discover_coaches()
    if not coaches:
        print("📭 No coaches configured. Add coach_telegram_config.yaml to production/ folders.")
        return

    print(f"📋 Found {len(coaches)} configured coach(es)")
    print()

    sent_count = 0
    for coach in coaches:
        name = coach["name"]
        config = coach["config"]
        coach_dir = coach["dir"]

        day = config.get("delivery", {}).get("day", "thursday")
        tz = config.get("delivery", {}).get("timezone", "UTC")
        time_str = config.get("delivery", {}).get("time", "09:00")

        if not should_send_today(config):
            print(f"⏭️  {name}: Not today (scheduled: {day})")
            continue

        if not is_within_delivery_window(config):
            print(f"⏰ {name}: Today is {day} but not yet {time_str} ({tz})")
            continue

        if has_sent_this_week(coach_dir):
            print(f"✅ {name}: Already sent this week")
            continue

        print(f"📤 {name}: Sending ideas (it's {day} in {tz})!")
        run_bot_for_coach(name, coach_dir)
        sent_count += 1

    print(f"\n📊 Summary: {sent_count}/{len(coaches)} coaches sent today.")


def run_daemon():
    """Keep running, check every hour."""
    print("🔄 Starting scheduler daemon (checking every hour)...")
    print("   Press Ctrl+C to stop.\n")

    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"⏰ [{now}] Running check...")
        run_check()
        print(f"\n💤 Sleeping for 1 hour...\n")
        time.sleep(3600)


def list_coaches():
    """List all configured coaches and their schedules."""
    coaches = discover_coaches()
    if not coaches:
        print("📭 No coaches configured.")
        return

    print(f"📋 Configured Coaches ({len(coaches)}):\n")
    print(f"{'Coach':<20} {'Day':<12} {'Time':<8} {'Timezone':<16} {'Format':<10} {'Chat ID'}")
    print("─" * 85)

    for coach in coaches:
        config = coach["config"]
        delivery = config.get("delivery", {})
        telegram = config.get("telegram", {})
        content = config.get("content", {})

        name = coach["name"][:20]
        day = delivery.get("day", "thursday")
        time_str = delivery.get("time", "09:00")
        tz = delivery.get("timezone", "UTC")[:16]
        fmt = content.get("format", "mixed")
        chat_id = telegram.get("chat_id", "NOT SET")

        status = "✅" if chat_id and chat_id != "NOT SET" else "❌"
        print(f"{status} {name:<18} {day:<12} {time_str:<8} {tz:<16} {fmt:<10} {chat_id}")


def main():
    parser = argparse.ArgumentParser(description="Daily scheduler for Tier List Bot")
    parser.add_argument("--daemon", action="store_true", help="Run continuously, checking every hour")
    parser.add_argument("--list", action="store_true", help="List all configured coaches")

    args = parser.parse_args()

    # Load .env
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)

    if args.list:
        list_coaches()
    elif args.daemon:
        run_daemon()
    else:
        run_check()


if __name__ == "__main__":
    main()
