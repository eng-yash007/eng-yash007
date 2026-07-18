import json
from utils import COLORS, FONTS, save_svg
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def generate_codechef_svg():
    input_path = Path("data/codechef.json")
    if not input_path.exists():
        logging.warning("codechef.json not found. Run fetch_codechef.py first.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        stats = json.load(f)

    title_bar = f"""
    <rect width="100%" height="30" fill="{COLORS['border']}" rx="4" />
    <circle cx="15" cy="15" r="6" fill="#ff5f56"/>
    <circle cx="35" cy="15" r="6" fill="#ffbd2e"/>
    <circle cx="55" cy="15" r="6" fill="#27c93f"/>
    <text x="50%" y="20" class="text-primary" font-size="14" text-anchor="middle">yash@github: ~/codechef</text>
    """
    
    items = [
        ("Current Rating", stats.get("rating", 0)),
        ("Highest Rating", stats.get("highest_rating", 0)),
        ("Stars", stats.get("stars", "0★"))
    ]
    
    stats_ui = ""
    delay = 0.5
    for i, (label, value) in enumerate(items):
        stats_ui += f"""
        <g class="fade-in" style="animation-delay: {delay}s; opacity: 0;">
            <text x="40" y="{70 + i * 35}" font-size="14" class="text-accent">{label.ljust(15)}</text>
            <text x="180" y="{70 + i * 35}" font-size="14" class="text-primary">: {value}</text>
        </g>
        """
        delay += 0.2

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="180" viewBox="0 0 400 180">
    <style>
        .text-primary {{ font-family: {FONTS['primary']}; fill: {COLORS['primary']}; }}
        .text-accent {{ font-family: {FONTS['primary']}; fill: {COLORS['accent']}; }}
        .bg {{ fill: {COLORS['background']}; }}
        .border {{ stroke: {COLORS['border']}; fill: none; }}
        
        @keyframes slideInRight {{
            from {{ opacity: 0; transform: translateX(-20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        .fade-in {{
            animation: slideInRight 0.5s forwards ease-out;
        }}
    </style>
    
    <rect width="400" height="180" class="bg" rx="6" />
    <rect width="400" height="180" class="border" rx="6" stroke-width="2"/>
    
    {title_bar}
    {stats_ui}
</svg>"""

    save_svg("codechef.svg", svg_content)

if __name__ == "__main__":
    generate_codechef_svg()
