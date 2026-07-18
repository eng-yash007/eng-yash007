import json
from utils import COLORS, FONTS, save_svg
from pathlib import Path
import logging
import textwrap

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def generate_quote_svg():
    input_path = Path("data/quotes.json")
    if not input_path.exists():
        logging.warning("quotes.json not found. Run fetch_quote.py first.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    quote = data.get("quote", "")
    author = data.get("author", "")
    
    # Wrap text to fit SVG width
    wrapper = textwrap.TextWrapper(width=60)
    wrapped_quote = wrapper.wrap(text=quote)

    title_bar = f"""
    <rect width="100%" height="30" fill="{COLORS['border']}" rx="4" />
    <circle cx="15" cy="15" r="6" fill="#ff5f56"/>
    <circle cx="35" cy="15" r="6" fill="#ffbd2e"/>
    <circle cx="55" cy="15" r="6" fill="#27c93f"/>
    <text x="50%" y="20" class="text-primary" font-size="14" text-anchor="middle">yash@github: ~/quote</text>
    """
    
    svg_height = max(180, 80 + len(wrapped_quote) * 25 + 40)
    
    content_ui = f"""
    <g class="fade-in" style="animation-delay: 0.5s; opacity: 0;">
        <text x="30" y="60" font-size="14" class="text-accent">$ fortune</text>
    </g>
    """
    
    delay = 1.0
    for i, line in enumerate(wrapped_quote):
        # Escape special XML chars
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        content_ui += f"""
        <g class="fade-in" style="animation-delay: {delay}s; opacity: 0;">
            <text x="30" y="{90 + i * 25}" font-size="14" class="text-primary" font-style="italic">"{safe_line}"</text>
        </g>
        """
        delay += 0.2
        
    content_ui += f"""
    <g class="fade-in" style="animation-delay: {delay}s; opacity: 0;">
        <text x="30" y="{90 + len(wrapped_quote) * 25 + 10}" font-size="14" class="text-secondary">— {author}</text>
    </g>
    """

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="{svg_height}" viewBox="0 0 600 {svg_height}">
    <style>
        .text-primary {{ font-family: {FONTS['primary']}; fill: {COLORS['primary']}; }}
        .text-secondary {{ font-family: {FONTS['primary']}; fill: {COLORS['secondary']}; }}
        .text-accent {{ font-family: {FONTS['primary']}; fill: {COLORS['accent']}; }}
        .bg {{ fill: {COLORS['background']}; }}
        .border {{ stroke: {COLORS['border']}; fill: none; }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        .fade-in {{
            animation: fadeIn 0.5s forwards;
        }}
    </style>
    
    <rect width="600" height="{svg_height}" class="bg" rx="6" />
    <rect width="600" height="{svg_height}" class="border" rx="6" stroke-width="2"/>
    
    {title_bar}
    {content_ui}
</svg>"""

    save_svg("typing.svg", svg_content) # Name requested by user in prompt as typing.svg or footer

if __name__ == "__main__":
    generate_quote_svg()
