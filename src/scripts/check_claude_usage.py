#!/usr/bin/env python3
"""
🌙 Moon Dev's Quick Claude Usage Check
Built with love by Moon Dev 🚀

Quick check of current Claude API usage - perfect for holiday monitoring.

Usage:
    python src/scripts/check_claude_usage.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# Direct import to avoid loading all models
try:
    from termcolor import cprint
except ImportError:
    def cprint(text, color=None, attrs=None):
        print(text)


def load_daily_summary(data_dir: Path) -> dict:
    """Load daily summary directly from file"""
    summary_file = data_dir / "daily_summary.json"
    if not summary_file.exists():
        return {}
    with open(summary_file, 'r') as f:
        return json.load(f)


def get_summary(data_dir: Path, days: int = 7) -> dict:
    """Get usage summary for the last N days"""
    summary = load_daily_summary(data_dir)
    if not summary:
        return {"error": "No usage data yet"}

    # Sort by date and get last N days
    sorted_dates = sorted(summary.keys(), reverse=True)[:days]

    total_cost = sum(summary[d]["total_cost"] for d in sorted_dates)
    total_tokens = sum(summary[d]["total_tokens"] for d in sorted_dates)
    total_requests = sum(summary[d]["request_count"] for d in sorted_dates)

    return {
        "period_days": len(sorted_dates),
        "total_cost_usd": round(total_cost, 4),
        "total_tokens": total_tokens,
        "total_requests": total_requests,
        "avg_daily_cost": round(total_cost / max(len(sorted_dates), 1), 4),
        "avg_tokens_per_request": round(total_tokens / max(total_requests, 1), 0),
        "daily_breakdown": {d: summary[d] for d in sorted_dates}
    }


def main():
    cprint("\n🌙 Claude Usage Quick Check", "cyan", attrs=["bold"])
    cprint("-" * 40, "cyan")

    # Find data directory
    data_dir = Path(__file__).parent.parent / "data" / "token_usage"

    if not data_dir.exists():
        cprint("\n📭 No usage data directory yet", "yellow")
        cprint("   Token tracking will start when you run Claude-powered agents", "white")
        cprint(f"   Data will be stored in: {data_dir}\n", "white")
        return

    summary = get_summary(data_dir, days=7)

    if "error" in summary:
        cprint(f"\n📭 {summary['error']}", "yellow")
        cprint("   Run some agents to start tracking!\n", "white")
        return

    print(f"\n📅 Last {summary['period_days']} days:")
    print(f"   💰 Total Cost:     ${summary['total_cost_usd']:.4f}")
    print(f"   📊 Total Tokens:   {summary['total_tokens']:,}")
    print(f"   🔄 Total Requests: {summary['total_requests']}")
    print(f"\n📈 Averages:")
    print(f"   Daily Cost:      ${summary['avg_daily_cost']:.4f}")
    print(f"   Tokens/Request:  {summary['avg_tokens_per_request']:,.0f}")

    # Project monthly from 7-day average
    monthly_projection = summary['avg_daily_cost'] * 30
    cprint(f"\n🔮 30-Day Projection: ${monthly_projection:.2f}", "green")

    # Quick tier hint
    if monthly_projection < 5:
        tier_hint = "Free/Tier 1 should be fine"
    elif monthly_projection < 100:
        tier_hint = "Tier 1-2 recommended"
    elif monthly_projection < 500:
        tier_hint = "Tier 2-3 recommended"
    else:
        tier_hint = "Tier 3+ recommended"

    cprint(f"💡 {tier_hint}\n", "yellow")

    # Show daily breakdown
    if summary.get('daily_breakdown'):
        cprint("📆 Recent Days:", "white")
        for date, stats in sorted(summary['daily_breakdown'].items(), reverse=True)[:5]:
            cost = stats.get('total_cost', 0)
            reqs = stats.get('request_count', 0)
            print(f"   {date}: ${cost:.4f} ({reqs} requests)")
        print()


if __name__ == "__main__":
    main()
