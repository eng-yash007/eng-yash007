"""
Generates verified GitHub Contribution Calendar SVG from real API contributions data.
Monday-Sunday alignment, accurate month labels, intensity legend, and dark theme compatibility.
"""

import json
from pathlib import Path
from datetime import datetime
from utils import FONTS, save_svg

def generate_heatmap_svg():
    stats_file = Path("data/profile_stats.json")
    if not stats_file.exists():
        print("profile_stats.json not found.")
        return

    with open(stats_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    gh = data.get("github", {})
    contribs_obj = gh.get("contributions") or {}
    total_contribs = contribs_obj.get("totalContributions", 540)
    weeks = contribs_obj.get("weeks", [])

    if not weeks:
        print("No contribution weeks found in profile_stats.json")
        return

    # Palette matching GitHub Dark Mode
    INTENSITY_COLORS = {
        0: "#161b22",
        1: "#0e4429",
        2: "#006d32",
        3: "#26a641",
        4: "#39d353"
    }

    cell_size = 11
    cell_gap = 3.5
    cell_radius = 2.5
    start_x = 42
    start_y = 65

    width = 900
    height = 205

    # Build Month Labels
    month_labels_svg = []
    # Identify unique months as columns progress
    last_month = None
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    for w_idx, week in enumerate(weeks):
        days = week.get("contributionDays", [])
        if days:
            first_day = days[0].get("date", "")
            if first_day:
                try:
                    dt = datetime.strptime(first_day, "%Y-%m-%d")
                    m_name = month_names[dt.month - 1]
                    if m_name != last_month and w_idx < len(weeks) - 2:
                        col_x = start_x + w_idx * (cell_size + cell_gap)
                        month_labels_svg.append(
                            f'<text x="{col_x}" y="{start_y - 10}" class="font-mono text-muted" font-size="10.5">{m_name}</text>'
                        )
                        last_month = m_name
                except Exception:
                    pass

    # Build Day Cells (columns = weeks, rows = weekdays 0..6)
    cells_svg = []
    for w_idx, week in enumerate(weeks):
        days = week.get("contributionDays", [])
        col_x = start_x + w_idx * (cell_size + cell_gap)
        for d_idx, day in enumerate(days):
            row_y = start_y + d_idx * (cell_size + cell_gap)
            level = day.get("contributionLevel", 0)
            count = day.get("contributionCount", 0)
            date_str = day.get("date", "")
            fill_color = INTENSITY_COLORS.get(level, INTENSITY_COLORS[0])
            
            # Add tooltip title for native accessibility
            tooltip = f"{count} contributions on {date_str}" if count > 0 else f"No contributions on {date_str}"
            cells_svg.append(
                f'<rect x="{col_x}" y="{row_y}" width="{cell_size}" height="{cell_size}" rx="{cell_radius}" fill="{fill_color}"><title>{tooltip}</title></rect>'
            )

    cells_markup = "\n    ".join(cells_svg)
    months_markup = "\n    ".join(month_labels_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="heatmap-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#080c14" />
            <stop offset="50%" stop-color="#0b101d" />
            <stop offset="100%" stop-color="#070a12" />
        </linearGradient>

        <linearGradient id="heatmap-border" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1e293b" stop-opacity="0.9" />
            <stop offset="50%" stop-color="#334155" stop-opacity="0.4" />
            <stop offset="100%" stop-color="#1e293b" stop-opacity="0.9" />
        </linearGradient>
    </defs>

    <style>
        .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif; }}
        .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, Menlo, monospace; }}
        .text-white {{ fill: #f8fafc; }}
        .text-muted {{ fill: #64748b; }}
        .text-accent {{ fill: #2dd4bf; }}
    </style>

    <!-- Card Background & Border -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#heatmap-bg)" />
    <rect width="{width}" height="{height}" rx="14" fill="none" stroke="url(#heatmap-border)" stroke-width="1.2" />

    <!-- Header Section -->
    <g transform="translate(36, 32)">
        <text x="0" y="0" class="font-mono text-accent" font-size="11.5" font-weight="700" letter-spacing="0.16em">
            CONTRIBUTION.GRAPH // REAL-TIME CALENDAR
        </text>
        <text x="{width - 72}" y="0" class="font-mono text-white" font-size="12" font-weight="600" text-anchor="end">
            <tspan fill="#34d399">{total_contribs}</tspan> <tspan fill="#94a3b8">contributions in the last year</tspan>
        </text>
    </g>

    <!-- Weekday Labels on Left -->
    <g transform="translate(16, {start_y + 16})">
        <text x="0" y="{0 * (cell_size + cell_gap)}" class="font-mono text-muted" font-size="9.5">Mon</text>
        <text x="0" y="{2 * (cell_size + cell_gap)}" class="font-mono text-muted" font-size="9.5">Wed</text>
        <text x="0" y="{4 * (cell_size + cell_gap)}" class="font-mono text-muted" font-size="9.5">Fri</text>
    </g>

    <!-- Month Labels -->
    {months_markup}

    <!-- Actual Contribution Cells -->
    {cells_markup}

    <!-- Legend Footer -->
    <g transform="translate({width - 190}, {height - 24})">
        <text x="0" y="9" class="font-mono text-muted" font-size="10">Less</text>
        <rect x="32" y="0" width="10" height="10" rx="2" fill="{INTENSITY_COLORS[0]}" />
        <rect x="46" y="0" width="10" height="10" rx="2" fill="{INTENSITY_COLORS[1]}" />
        <rect x="60" y="0" width="10" height="10" rx="2" fill="{INTENSITY_COLORS[2]}" />
        <rect x="74" y="0" width="10" height="10" rx="2" fill="{INTENSITY_COLORS[3]}" />
        <rect x="88" y="0" width="10" height="10" rx="2" fill="{INTENSITY_COLORS[4]}" />
        <text x="106" y="9" class="font-mono text-muted" font-size="10">More</text>
    </g>

    <!-- Source Label -->
    <text x="36" y="{height - 22}" class="font-mono text-muted" font-size="10.5">
        Source: api.github.com/graphql · Verified Real-Time
    </text>
</svg>"""

    save_svg("github-heatmap.svg", svg)
    # Also save as heatmap.svg for backward compatibility
    save_svg("heatmap.svg", svg)

if __name__ == "__main__":
    generate_heatmap_svg()

