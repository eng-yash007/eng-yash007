import json
from pathlib import Path
from utils import THEME, FONTS, escape, save_svg

def generate_stats_svg():
    # Load Stats
    stats_file = Path("data/stats.json")
    stats = {"repos": 10, "stars": 3, "followers": 1}
    if stats_file.exists():
        try:
            with open(stats_file, "r", encoding="utf-8") as f:
                stats = json.load(f)
        except Exception:
            pass

    # Load Leetcode
    lc_file = Path("data/leetcode.json")
    lc = {"totalSolved": 125, "easySolved": 50, "mediumSolved": 60, "hardSolved": 15}
    if lc_file.exists():
        try:
            with open(lc_file, "r", encoding="utf-8") as f:
                lc = json.load(f)
        except Exception:
            pass

    width = 900
    height = 200

    total_solved = lc.get("totalSolved", 125)
    easy = lc.get("easySolved", 50)
    med = lc.get("mediumSolved", 60)
    hard = lc.get("hardSolved", 15)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="metric-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#080b12" />
            <stop offset="50%" stop-color="#0c111e" />
            <stop offset="100%" stop-color="#060910" />
        </linearGradient>

        <linearGradient id="metric-glow" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#334155" stop-opacity="0.8"/>
            <stop offset="50%" stop-color="#1e293b" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#334155" stop-opacity="0.8"/>
        </linearGradient>
    </defs>

    <style>
        .font-sans {{ font-family: {FONTS['sans']}; }}
        .font-mono {{ font-family: {FONTS['mono']}; }}
    </style>

    <!-- Background Frame -->
    <rect width="{width}" height="{height}" rx="16" fill="url(#metric-bg)" />
    <rect width="{width}" height="{height}" rx="16" fill="none" stroke="url(#metric-glow)" stroke-width="1.2" />

    <!-- Top Label -->
    <g transform="translate(36, 32)">
        <text x="0" y="0" class="font-mono" font-size="12" font-weight="700" fill="#38bdf8" letter-spacing="0.18em">
            SYSTEM.METRICS // GITHUB &amp; PROBLEM SOLVING
        </text>
    </g>

    <!-- SECTION 1: GitHub Core Stats -->
    <g transform="translate(36, 64)">
        <rect width="250" height="106" rx="12" fill="#0f172a" fill-opacity="0.7" stroke="#1e293b" stroke-width="1.2"/>
        
        <text x="20" y="32" class="font-mono" font-size="11" font-weight="600" fill="#64748b">GITHUB REPOSITORIES</text>
        <text x="20" y="66" class="font-sans" font-size="28" font-weight="800" fill="#f8fafc">
            {stats.get('repos', 10)} <tspan font-size="14" font-weight="500" fill="#94a3b8">repos</tspan>
        </text>
        
        <text x="145" y="32" class="font-mono" font-size="11" font-weight="600" fill="#64748b">TOTAL STARS</text>
        <text x="145" y="66" class="font-sans" font-size="28" font-weight="800" fill="#fbbf24">
            {stats.get('stars', 3)}★
        </text>
    </g>

    <!-- SECTION 2: LeetCode Metrics -->
    <g transform="translate(310, 64)">
        <rect width="320" height="106" rx="12" fill="#0f172a" fill-opacity="0.7" stroke="#1e293b" stroke-width="1.2"/>
        
        <!-- Left Sub-block: Total Solved -->
        <g transform="translate(20, 24)">
            <text x="0" y="8" class="font-mono" font-size="11" font-weight="600" fill="#64748b">LEETCODE PROBLEMS</text>
            <text x="0" y="44" class="font-sans" font-size="30" font-weight="800" fill="#2dd4bf">
                {total_solved}+
            </text>
            <text x="0" y="64" class="font-mono" font-size="10.5" fill="#94a3b8">DSA &amp; Competitive</text>
        </g>

        <!-- Right Sub-block: Breakdown -->
        <g transform="translate(170, 24)">
            <!-- Easy -->
            <text x="0" y="10" class="font-mono" font-size="11" fill="#34d399">Easy: {easy}</text>
            <rect x="0" y="16" width="120" height="4" rx="2" fill="#1e293b"/>
            <rect x="0" y="16" width="60" height="4" rx="2" fill="#34d399"/>

            <!-- Medium -->
            <text x="0" y="36" class="font-mono" font-size="11" fill="#fbbf24">Medium: {med}</text>
            <rect x="0" y="42" width="120" height="4" rx="2" fill="#1e293b"/>
            <rect x="0" y="42" width="75" height="4" rx="2" fill="#fbbf24"/>

            <!-- Hard -->
            <text x="0" y="62" class="font-mono" font-size="11" fill="#f43f5e">Hard: {hard}</text>
            <rect x="0" y="68" width="120" height="4" rx="2" fill="#1e293b"/>
            <rect x="0" y="68" width="25" height="4" rx="2" fill="#f43f5e"/>
        </g>
    </g>

    <!-- SECTION 3: System Status & Work -->
    <g transform="translate(654, 64)">
        <rect width="210" height="106" rx="12" fill="#0f172a" fill-opacity="0.7" stroke="#1e293b" stroke-width="1.2"/>
        
        <text x="18" y="32" class="font-mono" font-size="11" font-weight="600" fill="#64748b">SYSTEM TELEMETRY</text>
        <text x="18" y="60" class="font-sans" font-size="15" font-weight="700" fill="#818cf8">
            FastAPI + pgvector
        </text>
        
        <g transform="translate(18, 76)">
            <circle cx="5" cy="5" r="4" fill="#10b981"/>
            <text x="16" y="9" class="font-mono" font-size="11" fill="#94a3b8">Active: Inference</text>
        </g>
    </g>
</svg>"""

    save_svg("stats.svg", svg)

if __name__ == "__main__":
    generate_stats_svg()
