import json
from utils import COLORS, FONTS, save_svg
from pathlib import Path

def generate_projects_svg():
    title_bar = f"""
    <rect width="100%" height="30" fill="{COLORS['border']}" rx="4" />
    <circle cx="15" cy="15" r="6" fill="#ff5f56"/>
    <circle cx="35" cy="15" r="6" fill="#ffbd2e"/>
    <circle cx="55" cy="15" r="6" fill="#27c93f"/>
    <text x="50%" y="20" class="text-primary" font-size="14" text-anchor="middle">yash@github: ~/projects</text>
    """
    
    projects = [
        "Silent Gallery",
        "DocuDost",
        "Traffic Management",
        "Murliwala Sarees"
    ]
    
    tree_ui = f"""
    <g class="fade-in" style="animation-delay: 0.5s; opacity: 0;">
        <text x="30" y="70" font-size="14" class="text-accent">projects/</text>
    </g>
    """
    
    delay = 0.8
    for i, proj in enumerate(projects):
        is_last = (i == len(projects) - 1)
        branch = "└──" if is_last else "├──"
        
        tree_ui += f"""
        <g class="fade-in" style="animation-delay: {delay}s; opacity: 0;">
            <text x="30" y="{100 + i * 25}" font-size="14" class="text-secondary">{branch} </text>
            <text x="65" y="{100 + i * 25}" font-size="14" class="text-primary">{proj}</text>
        </g>
        """
        delay += 0.3

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="220" viewBox="0 0 400 220">
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
            animation: fadeIn 0.4s forwards ease-in-out;
        }}
    </style>
    
    <rect width="400" height="220" class="bg" rx="6" />
    <rect width="400" height="220" class="border" rx="6" stroke-width="2"/>
    
    {title_bar}
    {tree_ui}
</svg>"""

    save_svg("projects.svg", svg_content)

if __name__ == "__main__":
    generate_projects_svg()
