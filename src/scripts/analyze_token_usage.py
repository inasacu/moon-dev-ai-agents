#!/usr/bin/env python3
"""
🌙 Moon Dev's Claude Token Usage Analyzer
Built with love by Moon Dev 🚀

Run this script mid-January to analyze 3 weeks of Claude API usage
and determine if you should upgrade to a higher tier.

Usage:
    python src/scripts/analyze_token_usage.py
    python src/scripts/analyze_token_usage.py --days 21
    python src/scripts/analyze_token_usage.py --detailed
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import csv
import json
from collections import defaultdict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from termcolor import cprint

# Anthropic API Tier Information (as of Dec 2024)
ANTHROPIC_TIERS = {
    "Free": {
        "monthly_limit": 0,
        "rate_limits": {"rpm": 5, "tpm": 20000, "rpd": 100},
        "cost": 0
    },
    "Build (Tier 1)": {
        "monthly_limit": 100,
        "rate_limits": {"rpm": 50, "tpm": 40000, "rpd": 1000},
        "cost": "Pay as you go ($5 min deposit)"
    },
    "Build (Tier 2)": {
        "monthly_limit": 500,
        "rate_limits": {"rpm": 1000, "tpm": 80000, "rpd": 10000},
        "cost": "Pay as you go ($40 min)"
    },
    "Build (Tier 3)": {
        "monthly_limit": 1000,
        "rate_limits": {"rpm": 2000, "tpm": 160000, "rpd": 20000},
        "cost": "Pay as you go ($200 min)"
    },
    "Build (Tier 4)": {
        "monthly_limit": 5000,
        "rate_limits": {"rpm": 4000, "tpm": 400000, "rpd": 100000},
        "cost": "Pay as you go ($400 min)"
    },
    "Scale": {
        "monthly_limit": "Custom",
        "rate_limits": "Custom",
        "cost": "Contact sales"
    }
}


def load_usage_data(data_dir: Path) -> list:
    """Load all usage data from CSV"""
    usage_file = data_dir / "claude_usage.csv"
    if not usage_file.exists():
        return []

    data = []
    with open(usage_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['input_tokens'] = int(row['input_tokens'])
            row['output_tokens'] = int(row['output_tokens'])
            row['total_tokens'] = int(row['total_tokens'])
            row['total_cost_usd'] = float(row['total_cost_usd'])
            row['timestamp'] = datetime.fromisoformat(row['timestamp'])
            data.append(row)
    return data


def analyze_usage(data: list, days: int = 21) -> dict:
    """Analyze usage patterns"""
    if not data:
        return {"error": "No data available"}

    cutoff = datetime.now() - timedelta(days=days)
    filtered = [d for d in data if d['timestamp'] > cutoff]

    if not filtered:
        return {"error": f"No data in the last {days} days"}

    # Basic stats
    total_cost = sum(d['total_cost_usd'] for d in filtered)
    total_tokens = sum(d['total_tokens'] for d in filtered)
    total_requests = len(filtered)

    # Daily breakdown
    daily_stats = defaultdict(lambda: {"cost": 0, "tokens": 0, "requests": 0})
    for d in filtered:
        date = d['date']
        daily_stats[date]["cost"] += d['total_cost_usd']
        daily_stats[date]["tokens"] += d['total_tokens']
        daily_stats[date]["requests"] += 1

    # Hourly distribution (for rate limit analysis)
    hourly_requests = defaultdict(int)
    for d in filtered:
        hourly_requests[d['hour']] += 1

    # Model breakdown
    model_stats = defaultdict(lambda: {"cost": 0, "tokens": 0, "requests": 0})
    for d in filtered:
        model = d['model']
        model_stats[model]["cost"] += d['total_cost_usd']
        model_stats[model]["tokens"] += d['total_tokens']
        model_stats[model]["requests"] += 1

    # Agent breakdown
    agent_stats = defaultdict(lambda: {"cost": 0, "tokens": 0, "requests": 0})
    for d in filtered:
        agent = d.get('agent_name', 'unknown')
        agent_stats[agent]["cost"] += d['total_cost_usd']
        agent_stats[agent]["tokens"] += d['total_tokens']
        agent_stats[agent]["requests"] += 1

    # Calculate actual days with data
    actual_days = len(daily_stats)
    avg_daily_cost = total_cost / actual_days if actual_days > 0 else 0

    # Project monthly usage
    projected_monthly_cost = avg_daily_cost * 30
    projected_monthly_tokens = (total_tokens / actual_days) * 30 if actual_days > 0 else 0

    # Peak hour analysis
    peak_hour = max(hourly_requests, key=hourly_requests.get) if hourly_requests else 0
    peak_requests_per_hour = max(hourly_requests.values()) if hourly_requests else 0

    return {
        "period": {
            "requested_days": days,
            "actual_days_with_data": actual_days,
            "start_date": min(d['date'] for d in filtered),
            "end_date": max(d['date'] for d in filtered)
        },
        "totals": {
            "cost_usd": round(total_cost, 4),
            "tokens": total_tokens,
            "requests": total_requests
        },
        "averages": {
            "daily_cost_usd": round(avg_daily_cost, 4),
            "daily_tokens": round(total_tokens / actual_days, 0) if actual_days > 0 else 0,
            "daily_requests": round(total_requests / actual_days, 1) if actual_days > 0 else 0,
            "tokens_per_request": round(total_tokens / total_requests, 0) if total_requests > 0 else 0
        },
        "projections": {
            "monthly_cost_usd": round(projected_monthly_cost, 2),
            "monthly_tokens": round(projected_monthly_tokens, 0)
        },
        "rate_limits": {
            "peak_hour": peak_hour,
            "peak_requests_in_hour": peak_requests_per_hour,
            "max_requests_per_minute_observed": peak_requests_per_hour / 60  # rough estimate
        },
        "by_model": dict(model_stats),
        "by_agent": dict(agent_stats),
        "daily_breakdown": dict(daily_stats)
    }


def recommend_tier(analysis: dict) -> dict:
    """Recommend an appropriate tier based on usage"""
    if "error" in analysis:
        return {"recommendation": "Insufficient data", "reason": analysis["error"]}

    monthly_cost = analysis["projections"]["monthly_cost_usd"]
    peak_rpm = analysis["rate_limits"]["max_requests_per_minute_observed"]

    # Find appropriate tier
    recommended = "Free"
    reason = []

    # Cost-based recommendation
    if monthly_cost > 0:
        recommended = "Build (Tier 1)"
        reason.append(f"Projected monthly spend: ${monthly_cost:.2f}")

    if monthly_cost > 100:
        recommended = "Build (Tier 2)"
        reason.append("Monthly spend exceeds $100")

    if monthly_cost > 500:
        recommended = "Build (Tier 3)"
        reason.append("Monthly spend exceeds $500")

    if monthly_cost > 1000:
        recommended = "Build (Tier 4)"
        reason.append("Monthly spend exceeds $1000")

    if monthly_cost > 5000:
        recommended = "Scale"
        reason.append("Monthly spend exceeds $5000 - contact Anthropic sales")

    # Rate limit based check
    tier_info = ANTHROPIC_TIERS.get(recommended, {})
    if isinstance(tier_info.get("rate_limits"), dict):
        tier_rpm = tier_info["rate_limits"]["rpm"]
        if peak_rpm > tier_rpm * 0.8:
            reason.append(f"Peak RPM ({peak_rpm:.1f}) approaching tier limit ({tier_rpm})")
            # Suggest next tier
            tier_names = list(ANTHROPIC_TIERS.keys())
            current_idx = tier_names.index(recommended) if recommended in tier_names else 0
            if current_idx < len(tier_names) - 1:
                recommended = tier_names[current_idx + 1]
                reason.append(f"Consider upgrading for headroom")

    return {
        "current_analysis_period": f"{analysis['period']['actual_days_with_data']} days",
        "recommended_tier": recommended,
        "tier_details": ANTHROPIC_TIERS.get(recommended, {}),
        "reasons": reason,
        "projected_monthly": {
            "cost_usd": monthly_cost,
            "tokens": analysis["projections"]["monthly_tokens"]
        },
        "usage_intensity": "Low" if monthly_cost < 50 else "Medium" if monthly_cost < 200 else "High"
    }


def print_report(analysis: dict, recommendation: dict, detailed: bool = False):
    """Print a formatted report"""
    cprint("\n" + "="*60, "cyan")
    cprint("🌙 CLAUDE TOKEN USAGE ANALYSIS REPORT", "cyan", attrs=["bold"])
    cprint("="*60 + "\n", "cyan")

    if "error" in analysis:
        cprint(f"❌ {analysis['error']}", "red")
        return

    # Period
    cprint("📅 ANALYSIS PERIOD", "yellow", attrs=["bold"])
    print(f"   Start: {analysis['period']['start_date']}")
    print(f"   End:   {analysis['period']['end_date']}")
    print(f"   Days with data: {analysis['period']['actual_days_with_data']}")
    print()

    # Totals
    cprint("📊 TOTALS", "yellow", attrs=["bold"])
    print(f"   Total Cost:     ${analysis['totals']['cost_usd']:.4f}")
    print(f"   Total Tokens:   {analysis['totals']['tokens']:,}")
    print(f"   Total Requests: {analysis['totals']['requests']:,}")
    print()

    # Averages
    cprint("📈 DAILY AVERAGES", "yellow", attrs=["bold"])
    print(f"   Cost/Day:       ${analysis['averages']['daily_cost_usd']:.4f}")
    print(f"   Tokens/Day:     {analysis['averages']['daily_tokens']:,.0f}")
    print(f"   Requests/Day:   {analysis['averages']['daily_requests']:.1f}")
    print(f"   Tokens/Request: {analysis['averages']['tokens_per_request']:,.0f}")
    print()

    # Projections
    cprint("🔮 MONTHLY PROJECTIONS", "yellow", attrs=["bold"])
    print(f"   Projected Cost:   ${analysis['projections']['monthly_cost_usd']:.2f}")
    print(f"   Projected Tokens: {analysis['projections']['monthly_tokens']:,.0f}")
    print()

    # Model breakdown
    if analysis['by_model']:
        cprint("🤖 BY MODEL", "yellow", attrs=["bold"])
        for model, stats in sorted(analysis['by_model'].items(), key=lambda x: x[1]['cost'], reverse=True):
            print(f"   {model}:")
            print(f"      Cost: ${stats['cost']:.4f} | Requests: {stats['requests']} | Tokens: {stats['tokens']:,}")
        print()

    # Agent breakdown
    if analysis['by_agent'] and detailed:
        cprint("🤖 BY AGENT", "yellow", attrs=["bold"])
        for agent, stats in sorted(analysis['by_agent'].items(), key=lambda x: x[1]['cost'], reverse=True):
            print(f"   {agent}:")
            print(f"      Cost: ${stats['cost']:.4f} | Requests: {stats['requests']} | Tokens: {stats['tokens']:,}")
        print()

    # Daily breakdown (if detailed)
    if detailed and analysis['daily_breakdown']:
        cprint("📆 DAILY BREAKDOWN", "yellow", attrs=["bold"])
        for date, stats in sorted(analysis['daily_breakdown'].items()):
            print(f"   {date}: ${stats['cost']:.4f} | {stats['requests']} req | {stats['tokens']:,} tokens")
        print()

    # Recommendation
    cprint("="*60, "green")
    cprint("💡 TIER RECOMMENDATION", "green", attrs=["bold"])
    cprint("="*60, "green")
    print()
    cprint(f"   Recommended Tier: {recommendation['recommended_tier']}", "white", attrs=["bold"])
    print(f"   Usage Intensity:  {recommendation['usage_intensity']}")
    print()

    if recommendation['reasons']:
        cprint("   Reasons:", "white")
        for reason in recommendation['reasons']:
            print(f"      • {reason}")
    print()

    tier_details = recommendation.get('tier_details', {})
    if tier_details:
        cprint("   Tier Details:", "white")
        if isinstance(tier_details.get('rate_limits'), dict):
            rl = tier_details['rate_limits']
            print(f"      Rate Limits: {rl.get('rpm', 'N/A')} RPM | {rl.get('tpm', 'N/A')} TPM | {rl.get('rpd', 'N/A')} RPD")
        print(f"      Monthly Limit: ${tier_details.get('monthly_limit', 'N/A')}")
        print(f"      Cost: {tier_details.get('cost', 'N/A')}")
    print()

    # Holiday reminder
    cprint("🎄 HOLIDAY NOTES", "magenta", attrs=["bold"])
    print("   • This analysis covers your holiday period usage")
    print("   • Normal work usage may be higher - factor in ~20-50% buffer")
    print("   • Re-run this analysis mid-January before making tier decisions")
    print()


def main():
    parser = argparse.ArgumentParser(description="Analyze Claude token usage")
    parser.add_argument("--days", type=int, default=21, help="Number of days to analyze (default: 21)")
    parser.add_argument("--detailed", action="store_true", help="Show detailed breakdown")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    data_dir = Path(__file__).parent.parent / "data" / "token_usage"

    if not data_dir.exists():
        cprint("❌ No usage data directory found at src/data/token_usage/", "red")
        cprint("   Token tracking hasn't started yet - run some agents first!", "yellow")
        return

    data = load_usage_data(data_dir)
    if not data:
        cprint("❌ No usage data found yet", "red")
        cprint("   Run some agents that use Claude to start collecting data", "yellow")
        return

    analysis = analyze_usage(data, days=args.days)
    recommendation = recommend_tier(analysis)

    if args.json:
        output = {
            "analysis": analysis,
            "recommendation": recommendation,
            "generated_at": datetime.now().isoformat()
        }
        print(json.dumps(output, indent=2, default=str))
    else:
        print_report(analysis, recommendation, detailed=args.detailed)


if __name__ == "__main__":
    main()
