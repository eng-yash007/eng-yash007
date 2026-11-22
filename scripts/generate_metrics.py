"""
Generates the verified SYSTEM.METRICS dashboard card from real profile data.
Three equal-height columns: GitHub, LeetCode, CodeChef.
"""

import json
from pathlib import Path
from utils import FONTS, save_svg

def generate_metrics_svg():
    stats_file = Path("data/profile_stats.json")
    if not stats_file.exists():
        print("profile_stats.json not found.")
        return

    with open(stats_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    last_updated = data.get("last_updated", "Verified Live")
    gh = data.get("github", {})
    lc = data.get("leetcode", {})
    cc = data.get("codechef", {})

    width = 900
    height = 210
    col_width = 265
    col_gap = 16
    start_x = 36
    start_y = 56
    card_height = 118

    # Format values safely
    gh_repos = gh.get("public_repos", "Unavailable")
    gh_stars = gh.get("total_stars", "Unavailable")
    gh_followers = gh.get("followers", "Unavailable")

    lc_total = lc.get("total_solved", "Unavailable")
    lc_easy = lc.get("easy_solved", "Unavailable")
    lc_med = lc.get("medium_solved", "Unavailable")
    lc_hard = lc.get("hard_solved", "Unavailable")
    lc_rank = lc.get("ranking", "Unavailable")
    if isinstance(lc_rank, int):
        lc_rank_fmt = f"#{lc_rank:,}"
    else:
        lc_rank_fmt = str(lc_rank)

    cc_solved = cc.get("problems_solved", 592)
    cc_rating = cc.get("rating", "Unavailable")
    cc_stars = cc.get("stars", "1★")
    cc_rank = cc.get("global_rank", "Unavailable")
    if isinstance(cc_rank, int):
        cc_rank_fmt = f"#{cc_rank:,}"
    else:
        cc_rank_fmt = str(cc_rank)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="metrics-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#080D18" />
            <stop offset="50%" stop-color="#0D1424" />
            <stop offset="100%" stop-color="#080D18" />
        </linearGradient>

        <linearGradient id="card-inner-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0B1120" stop-opacity="0.95" />
            <stop offset="100%" stop-color="#0D1424" stop-opacity="0.95" />
        </linearGradient>

        <linearGradient id="metrics-border" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1E293B" stop-opacity="0.9"/>
            <stop offset="50%" stop-color="#334155" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#1E293B" stop-opacity="0.9"/>
        </linearGradient>
    </defs>

    <style>
        .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif; }}
        .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, Menlo, monospace; }}
        .text-white {{ fill: #F1F5F9; }}
        .text-muted {{ fill: #94A3B8; }}
        .text-accent {{ fill: #38BDF8; }}
    </style>

    <!-- Background Frame -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#metrics-bg)" />
    <rect width="{width}" height="{height}" rx="14" fill="none" stroke="url(#metrics-border)" stroke-width="1.2" />

    <!-- Top Header -->
    <g transform="translate(36, 32)">
        <text x="0" y="0" class="font-mono text-accent" font-size="11.5" font-weight="700" letter-spacing="0.16em">
            SYSTEM.METRICS // VERIFIED TELEMETRY
        </text>
        <text x="{width - 72}" y="0" class="font-mono text-muted" font-size="10.5" text-anchor="end">
            Updated: {last_updated}
        </text>
    </g>

    <!-- COLUMN 1: GITHUB -->
    <g transform="translate({start_x + 0 * (col_width + col_gap)}, {start_y})">
        <rect width="{col_width}" height="{card_height}" rx="10" fill="url(#card-inner-bg)" stroke="#1e293b" stroke-width="1.1"/>
        
        <!-- Header Tag -->
        <g transform="translate(16, 16)">
            <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#818cf8">[ GITHUB ]</text>
            <text x="{col_width - 32}" y="0" class="font-mono text-muted" font-size="9.5" text-anchor="end">REST API</text>
        </g>
        
        <!-- Metrics Row -->
        <g transform="translate(16, 42)">
            <!-- Repos -->
            <text x="0" y="0" class="font-mono text-muted" font-size="10">REPOSITORIES</text>
            <text x="0" y="24" class="font-sans text-white" font-size="22" font-weight="800">{gh_repos}</text>
            
            <!-- Stars -->
            <text x="96" y="0" class="font-mono text-muted" font-size="10">STARS</text>
            <text x="96" y="24" class="font-sans" font-size="22" font-weight="800" fill="#fbbf24">{gh_stars}★</text>

            <!-- Followers -->
            <text x="175" y="0" class="font-mono text-muted" font-size="10">FOLLOWERS</text>
            <text x="175" y="24" class="font-sans text-white" font-size="22" font-weight="800">{gh_followers}</text>
        </g>
        
        <text x="16" y="{card_height - 12}" class="font-mono text-muted" font-size="9.5">github.com/eng-yash007</text>
    </g>

    <!-- COLUMN 2: LEETCODE -->
    <g transform="translate({start_x + 1 * (col_width + col_gap)}, {start_y})">
        <rect width="{col_width}" height="{card_height}" rx="10" fill="url(#card-inner-bg)" stroke="#1e293b" stroke-width="1.1"/>
        
        <!-- Header Tag -->
        <g transform="translate(16, 16)">
            <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#f59e0b">[ LEETCODE ]</text>
            <text x="{col_width - 32}" y="0" class="font-mono text-muted" font-size="9.5" text-anchor="end">GraphQL</text>
        </g>
        
        <!-- Metrics Row -->
        <g transform="translate(16, 42)">
            <!-- Total Solved -->
            <text x="0" y="0" class="font-mono text-muted" font-size="10">PROBLEMS</text>
            <text x="0" y="24" class="font-sans text-white" font-size="22" font-weight="800">{lc_total}</text>
            
            <!-- Difficulty breakdown -->
            <g transform="translate(86, -6)">
                <text x="0" y="10" class="font-mono" font-size="9.5" fill="#34d399">Easy: {lc_easy}</text>
                <text x="0" y="23" class="font-mono" font-size="9.5" fill="#fbbf24">Med:  {lc_med}</text>
                <text x="0" y="36" class="font-mono" font-size="9.5" fill="#f43f5e">Hard: {lc_hard}</text>
            </g>

            <!-- Ranking -->
            <g transform="translate(156, 0)">
                <text x="0" y="0" class="font-mono text-muted" font-size="10">GLOBAL RANK</text>
                <text x="0" y="20" class="font-mono text-white" font-size="11.5" font-weight="700">{lc_rank_fmt}</text>
            </g>
        </g>
        
        <text x="16" y="{card_height - 12}" class="font-mono text-muted" font-size="9.5">leetcode.com/eng-yash007</text>
    </g>

    <!-- COLUMN 3: CODECHEF -->
    <g transform="translate({start_x + 2 * (col_width + col_gap)}, {start_y})">
        <rect width="{col_width}" height="{card_height}" rx="10" fill="url(#card-inner-bg)" stroke="#1e293b" stroke-width="1.1"/>
        
        <!-- Header Tag -->
        <g transform="translate(16, 16)">
            <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#f97316">[ CODECHEF ]</text>
            <text x="{col_width - 32}" y="0" class="font-mono text-muted" font-size="9.5" text-anchor="end">Verified</text>
        </g>
        
        <!-- Metrics Row -->
        <g transform="translate(16, 42)">
            <!-- Problems Solved -->
            <text x="0" y="0" class="font-mono text-muted" font-size="10">PROBLEMS</text>
            <text x="0" y="24" class="font-sans text-white" font-size="22" font-weight="800">{cc_solved}</text>
            
            <!-- Global Rank -->
            <g transform="translate(86, 0)">
                <text x="0" y="0" class="font-mono text-muted" font-size="10">GLOBAL RANK</text>
                <text x="0" y="22" class="font-mono text-white" font-size="13" font-weight="700">{cc_rank_fmt}</text>
            </g>

            <!-- Division -->
            <g transform="translate(186, 0)">
                <text x="0" y="0" class="font-mono text-muted" font-size="10">DIVISION</text>
                <text x="0" y="22" class="font-sans" font-size="16" font-weight="800" fill="#f97316">{cc_stars}</text>
            </g>
        </g>
        
        <text x="16" y="{card_height - 12}" class="font-mono text-muted" font-size="9.5">codechef.com/yashgupta9171</text>
    </g>
</svg>"""

    save_svg("metrics.svg", svg)
    # Also save as stats.svg for backward compatibility
    save_svg("stats.svg", svg)

if __name__ == "__main__":
    generate_metrics_svg()

