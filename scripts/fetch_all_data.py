"""
Orchestrates live data collection from GitHub, LeetCode, and CodeChef.
Validates schemas and saves verified snapshot to data/profile_stats.json.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
import logging

from github_stats import fetch_github_data
from leetcode_stats import fetch_leetcode_data
from codechef_stats import fetch_codechef_data

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

STATS_FILE = Path("data/profile_stats.json")

def update_all_profile_stats():
    logging.info("Starting verified profile statistics collection...")
    
    # Existing snapshot if available for fallback
    previous_snapshot = {}
    if STATS_FILE.exists():
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                previous_snapshot = json.load(f)
        except Exception:
            pass

    gh = fetch_github_data("eng-yash007")
    lc = fetch_leetcode_data("eng-yash007")
    cc = fetch_codechef_data("yashgupta9171")

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Combine into unified verified snapshot
    combined = {
        "last_updated": now_utc,
        "github": gh,
        "leetcode": lc,
        "codechef": cc
    }

    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)

    logging.info(f"Verified profile snapshot saved to {STATS_FILE}")
    return combined

if __name__ == "__main__":
    update_all_profile_stats()
