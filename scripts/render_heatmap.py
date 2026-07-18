import json
from utils import COLORS, FONTS, save_svg
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def render_heatmap():
    input_path = Path("data/contributions.json")
    if not input_path.exists():
        logging.warning("contributions.json not found. Run fetch_contributions.py first.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    if not days:
        logging.warning("No contribution days found.")
        return

    # GitHub heatmap colors (Dark mode)
    LEVEL_COLORS = {
        0: "#161b22",
        1: "#0e4429",
        2: "#006d32",
        3: "#26a641",
        4: "#39d353"
    }

    # Group days by week (columns)
    # The scraped data is usually linear. We need 53 weeks x 7 days
    weeks = []
    current_week = []
    for day in days:
        current_week.append(day)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week)

    # Calculate SVG dimensions
    cell_size = 12
    gap = 4
    width = len(weeks) * (cell_size + gap) + 60
    height = 7 * (cell_size + gap) + 120 # Extra space for header/footer

    title_bar = f"""
    <rect width="100%" height="30" fill="{COLORS['border']}" rx="4" />
    <circle cx="15" cy="15" r="6" fill="#ff5f56"/>
    <circle cx="35" cy="15" r="6" fill="#ffbd2e"/>
    <circle cx="55" cy="15" r="6" fill="#27c93f"/>
    <text x="50%" y="20" class="text-primary" font-size="14" text-anchor="middle">yash@github: ~/heatmap</text>
    """

    rects = ""
    # Render diagonal reveal
    for col_idx, week in enumerate(weeks):
        for row_idx, day in enumerate(week):
            level = day.get("level", 0)
            color = LEVEL_COLORS.get(level, LEVEL_COLORS[0])
            
            x = 30 + col_idx * (cell_size + gap)
            y = 50 + row_idx * (cell_size + gap)
            
            # Diagonal delay = col_idx + row_idx
            delay = (col_idx + row_idx) * 0.02
            
            rects += f"""
            <rect class="cell" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}" style="animation-delay: {delay}s; opacity: 0; transform: scale(0.5); transform-origin: {x + cell_size/2}px {y + cell_size/2}px;"/>
            """

    # Legend
    legend_x = width - 150
    legend_y = 50 + 7 * (cell_size + gap) + 15
    legend = f"""
    <text x="{legend_x - 35}" y="{legend_y + 10}" font-size="12" class="text-secondary">Less</text>
    <rect x="{legend_x}" y="{legend_y}" width="12" height="12" rx="2" fill="{LEVEL_COLORS[0]}"/>
    <rect x="{legend_x + 16}" y="{legend_y}" width="12" height="12" rx="2" fill="{LEVEL_COLORS[1]}"/>
    <rect x="{legend_x + 32}" y="{legend_y}" width="12" height="12" rx="2" fill="{LEVEL_COLORS[2]}"/>
    <rect x="{legend_x + 48}" y="{legend_y}" width="12" height="12" rx="2" fill="{LEVEL_COLORS[3]}"/>
    <rect x="{legend_x + 64}" y="{legend_y}" width="12" height="12" rx="2" fill="{LEVEL_COLORS[4]}"/>
    <text x="{legend_x + 85}" y="{legend_y + 10}" font-size="12" class="text-secondary">More</text>
    """

    # Stats Footer
    footer_y = legend_y + 30
    stats = f"""
    <text x="30" y="{footer_y}" font-size="12" class="text-accent fade-in-up" style="animation-delay: 1.5s;">Total Contributions:</text>
    <text x="170" y="{footer_y}" font-size="12" class="text-primary fade-in-up" style="animation-delay: 1.5s;">{data.get('total', 0)}</text>
    
    <text x="250" y="{footer_y}" font-size="12" class="text-accent fade-in-up" style="animation-delay: 1.6s;">Current Streak:</text>
    <text x="360" y="{footer_y}" font-size="12" class="text-primary fade-in-up" style="animation-delay: 1.6s;">{data.get('current_streak', 0)} days</text>
    
    <text x="440" y="{footer_y}" font-size="12" class="text-accent fade-in-up" style="animation-delay: 1.7s;">Longest Streak:</text>
    <text x="550" y="{footer_y}" font-size="12" class="text-primary fade-in-up" style="animation-delay: 1.7s;">{data.get('longest_streak', 0)} days</text>
    
    <text x="630" y="{footer_y}" font-size="12" class="text-accent fade-in-up" style="animation-delay: 1.8s;">Best Day:</text>
    <text x="710" y="{footer_y}" font-size="12" class="text-primary fade-in-up" style="animation-delay: 1.8s;">{data.get('best_day_count', 0)}</text>
    """

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <style>
        .text-primary {{ font-family: {FONTS['primary']}; fill: {COLORS['primary']}; }}
        .text-secondary {{ font-family: {FONTS['primary']}; fill: {COLORS['secondary']}; }}
        .text-accent {{ font-family: {FONTS['primary']}; fill: {COLORS['accent']}; }}
        .bg {{ fill: {COLORS['background']}; }}
        .border {{ stroke: {COLORS['border']}; fill: none; }}
        
        @keyframes revealCell {{
            to {{ opacity: 1; transform: scale(1); }}
        }}
        .cell {{
            animation: revealCell 0.4s forwards cubic-bezier(0.1, 0.8, 0.2, 1);
        }}
        
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .fade-in-up {{
            opacity: 0;
            animation: fadeInUp 0.5s forwards ease-out;
        }}
    </style>
    
    <rect width="{width}" height="{height}" class="bg" rx="6" />
    <rect width="{width}" height="{height}" class="border" rx="6" stroke-width="2"/>
    
    {title_bar}
    {rects}
    {legend}
    {stats}
</svg>"""

    save_svg("heatmap.svg", svg_content)

if __name__ == "__main__":
    render_heatmap()
