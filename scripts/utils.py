"""
Utility functions and configuration constants for generating high-aesthetic SVGs.
Strictly adhering to the Premium Dark Tech Design System.
"""

from pathlib import Path
import html

# Premium Dark Tech Design Tokens
THEME = {
    "bg": "#080D18",
    "background": "#080D18",
    "bg_secondary": "#0D1424",
    "card_bg": "#0B1120",
    "card_bg_glass": "rgba(11, 17, 32, 0.90)",
    "border": "#1E293B",
    "border_subtle": "#334155",
    "electric_blue": "#38BDF8",
    "cyan": "#22D3EE",
    "violet": "#8B5CF6",
    "main_text": "#F1F5F9",
    "text_primary": "#F1F5F9",
    "text_white": "#F1F5F9",
    "secondary_text": "#94A3B8",
    "text_secondary": "#94A3B8",
    "text_muted": "#64748B",
    "accent_cyan": "#22D3EE",
    "accent_blue": "#38BDF8",
    "accent_violet": "#8B5CF6",
    "accent_green": "#34D399",
    "accent_amber": "#FBBF24",
    "accent_orange": "#FB923C",
    "accent_pink": "#F472B6"
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
