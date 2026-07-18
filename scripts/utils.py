"""
Utility functions and configuration constants for generating SVGs.
"""

from pathlib import Path

# Color Palette
COLORS = {
    "background": "#0d1117",
    "primary": "#c9d1d9",
    "secondary": "#8b949e",
    "accent": "#39d353",
    "border": "#30363d"
}

# Fonts
FONTS = {
    "primary": "JetBrains Mono, monospace",
    "fallback": "monospace"
}

def create_svg_container(width: int, height: int, content: str) -> str:
    """Wraps content in a standard SVG container with styling."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <style>
        .text-primary {{ font-family: {FONTS['primary']}; fill: {COLORS['primary']}; }}
        .text-secondary {{ font-family: {FONTS['primary']}; fill: {COLORS['secondary']}; }}
        .text-accent {{ font-family: {FONTS['primary']}; fill: {COLORS['accent']}; }}
        .bg {{ fill: {COLORS['background']}; }}
        .border {{ stroke: {COLORS['border']}; fill: none; }}
    </style>
    <rect width="{width}" height="{height}" class="bg" rx="10" />
    <rect width="{width}" height="{height}" class="border" rx="10" stroke-width="2"/>
    {content}
</svg>'''

def save_svg(filename: str, content: str):
    """Saves SVG content to the assets directory."""
    out_dir = Path("assets")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {out_path}")
