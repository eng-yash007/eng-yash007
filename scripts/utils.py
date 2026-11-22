"""
Utility functions and configuration constants for generating high-aesthetic SVGs.
"""

from pathlib import Path
import html

# Modern Dark Cyberpunk / Linear Portfolio Palette
THEME = {
    "bg": "#090d16",
    "background": "#090d16",
    "card_bg": "#0d131f",
    "card_bg_glass": "rgba(13, 19, 31, 0.85)",
    "border": "#1e293b",
    "border_glow": "#334155",
    "primary": "#e2e8f0",
    "secondary": "#94a3b8",
    "accent": "#2dd4bf",
    "text_white": "#ffffff",
    "text_primary": "#e2e8f0",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
    "accent_cyan": "#2dd4bf",
    "accent_indigo": "#818cf8",
    "accent_purple": "#c084fc",
    "accent_pink": "#f472b6",
    "accent_green": "#34d399",
    "accent_amber": "#fbbf24",
    "accent_orange": "#fb923c"
}

# Backward compatibility alias
COLORS = THEME

FONTS = {
    "sans": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, sans-serif",
    "mono": "'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, Menlo, monospace",
    "primary": "'JetBrains Mono', 'Fira Code', monospace",
    "fallback": "monospace"
}

def escape(text: str) -> str:
    """Escapes special characters for XML/SVG safety."""
    return html.escape(str(text))

def save_svg(filename: str, content: str):
    """Saves SVG content to the assets directory."""
    path = Path(filename)
    if not path.parts or path.parts[0] != "assets":
        path = Path("assets") / path
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generated {path}")
