"""
🌙 Moon Dev's Token Usage Tracker
Built with love by Moon Dev 🚀

Tracks Claude API token usage for cost analysis and tier planning.
Data stored in src/data/token_usage/ for 3-week analysis period.
"""

import os
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from threading import Lock
from termcolor import cprint

class TokenTracker:
    """Tracks Claude API token usage for cost analysis"""

    # Claude pricing per 1M tokens (as of Dec 2024)
    CLAUDE_PRICING = {
        # Claude 4 Series
        "claude-opus-4-5-20251101": {"input": 15.00, "output": 75.00},
        "claude-opus-4-1": {"input": 15.00, "output": 75.00},
        "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
        "claude-haiku-4-5": {"input": 0.80, "output": 4.00},
        # Claude 3.5 Series
        "claude-3-5-sonnet-latest": {"input": 3.00, "output": 15.00},
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-3-5-haiku-latest": {"input": 0.80, "output": 4.00},
        "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
        # Claude 3 Series
        "claude-3-opus": {"input": 15.00, "output": 75.00},
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        "claude-3-sonnet": {"input": 3.00, "output": 15.00},
        "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    }

    # Default pricing for unknown models
    DEFAULT_PRICING = {"input": 3.00, "output": 15.00}

    _instance = None
    _lock = Lock()

    def __new__(cls):
        """Singleton pattern for global tracking"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self._file_lock = Lock()

        # Set up data directory
        self.data_dir = Path(__file__).parent.parent / "data" / "token_usage"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Main usage log file
        self.usage_file = self.data_dir / "claude_usage.csv"
        self.daily_summary_file = self.data_dir / "daily_summary.json"

        # Initialize CSV if needed
        self._init_csv()

        cprint("📊 Token Tracker initialized - logging to src/data/token_usage/", "cyan")

    def _init_csv(self):
        """Initialize CSV file with headers if it doesn't exist"""
        if not self.usage_file.exists():
            with open(self.usage_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp',
                    'date',
                    'hour',
                    'model',
                    'agent_name',
                    'input_tokens',
                    'output_tokens',
                    'total_tokens',
                    'input_cost_usd',
                    'output_cost_usd',
                    'total_cost_usd',
                    'request_type'
                ])

    def get_pricing(self, model_name: str) -> Dict[str, float]:
        """Get pricing for a model"""
        # Try exact match first
        if model_name in self.CLAUDE_PRICING:
            return self.CLAUDE_PRICING[model_name]

        # Try prefix matching for versioned models
        for key in self.CLAUDE_PRICING:
            if model_name.startswith(key.split('-20')[0]):
                return self.CLAUDE_PRICING[key]

        return self.DEFAULT_PRICING

    def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> Dict[str, float]:
        """Calculate cost for a request"""
        pricing = self.get_pricing(model_name)

        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]

        return {
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": input_cost + output_cost
        }

    def log_usage(
        self,
        model_name: str,
        input_tokens: int,
        output_tokens: int,
        agent_name: str = "unknown",
        request_type: str = "generate"
    ):
        """Log a Claude API usage event"""
        now = datetime.now()
        costs = self.calculate_cost(model_name, input_tokens, output_tokens)

        row = [
            now.isoformat(),
            now.strftime('%Y-%m-%d'),
            now.hour,
            model_name,
            agent_name,
            input_tokens,
            output_tokens,
            input_tokens + output_tokens,
            f"{costs['input_cost']:.6f}",
            f"{costs['output_cost']:.6f}",
            f"{costs['total_cost']:.6f}",
            request_type
        ]

        with self._file_lock:
            with open(self.usage_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)

            # Update daily summary
            self._update_daily_summary(now.strftime('%Y-%m-%d'), costs['total_cost'], input_tokens + output_tokens)

    def _update_daily_summary(self, date: str, cost: float, tokens: int):
        """Update running daily summary"""
        summary = {}
        if self.daily_summary_file.exists():
            with open(self.daily_summary_file, 'r') as f:
                summary = json.load(f)

        if date not in summary:
            summary[date] = {"total_cost": 0, "total_tokens": 0, "request_count": 0}

        summary[date]["total_cost"] += cost
        summary[date]["total_tokens"] += tokens
        summary[date]["request_count"] += 1

        with open(self.daily_summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

    def get_summary(self, days: int = 7) -> Dict:
        """Get usage summary for the last N days"""
        if not self.daily_summary_file.exists():
            return {"error": "No usage data yet"}

        with open(self.daily_summary_file, 'r') as f:
            summary = json.load(f)

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


# Global singleton instance
token_tracker = TokenTracker()
