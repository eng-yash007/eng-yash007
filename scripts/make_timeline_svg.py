import json
from utils import COLORS, FONTS, save_svg

def generate_timeline():
    # Hardcoded timeline based on prompt
    events = [
        {"year": "2023", "text": "Started DSA & Development"},
        {"year": "2024", "text": "Computer Vision Intern - Ragh Vision"},
        {"year": "2024", "text": "Built Murliwala Sarees & Traffic Management"},
        {"year": "2025", "text": "GenAI Intern - Capri Global Capital Ltd."},
        {"year": "2025", "text": "Building Silent Gallery & DocuDost"}
    ]
    
    title_bar = f"""
    <rect width="100%" height="30" fill="{COLORS['border']}" rx="4" />
    <circle cx="15" cy="15" r="6" fill="#ff5f56"/>
    <circle cx="35" cy="15" r="6" fill="#ffbd2e"/>
    <circle cx="55" cy="15" r="6" fill="#27c93f"/>
    <text x="50%" y="20" class="text-primary" font-size="14" text-anchor="middle">yash@github: ~/timeline</text>
    """
    
    timeline_items = ""
    delay = 0.5
    for i, event in enumerate(events):
        year = event["year"]
        text = event["text"].replace("&", "&amp;")
        
        timeline_items += f"""
        <g class="fade-in" style="animation-delay: {delay}s; opacity: 0;">
            <text x="30" y="{70 + i * 40}" font-size="14" class="text-accent">{year}</text>
            <text x="80" y="{70 + i * 40}" font-size="14" class="text-primary">→ {text}</text>
        </g>
        """
        # Add connecting line except for the last item
        if i < len(events) - 1:
             timeline_items += f"""
             <g class="fade-in" style="animation-delay: {delay+0.2}s; opacity: 0;">
                <text x="45" y="{90 + i * 40}" font-size="14" class="text-secondary">↓</text>
             </g>
             """
        delay += 0.4

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="500" height="300" viewBox="0 0 500 300">
    <style>
        .text-primary {{ font-family: {FONTS['primary']}; fill: {COLORS['primary']}; }}
        .text-secondary {{ font-family: {FONTS['primary']}; fill: {COLORS['secondary']}; }}
        .text-accent {{ font-family: {FONTS['primary']}; fill: {COLORS['accent']}; }}
        .bg {{ fill: {COLORS['background']}; }}
        .border {{ stroke: {COLORS['border']}; fill: none; }}
        
        @keyframes slideDownFade {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .fade-in {{
            animation: slideDownFade 0.5s forwards ease-out;
        }}
    </style>
    
    <rect width="500" height="300" class="bg" rx="6" />
    <rect width="500" height="300" class="border" rx="6" stroke-width="2"/>
    
    {title_bar}
    {timeline_items}
</svg>"""

    save_svg("timeline.svg", svg_content)

if __name__ == "__main__":
    generate_timeline()
