import json
from utils import COLORS, FONTS, save_svg

def generate_skills():
    # Hardcoded skills based on prompt
    skills = [
        {"name": "Python", "level": 14},
        {"name": "FastAPI", "level": 10},
        {"name": "React", "level": 9},
        {"name": "Next.js", "level": 8},
        {"name": "OpenCV", "level": 8},
        {"name": "LangChain", "level": 9},
        {"name": "C++", "level": 12},
        {"name": "TypeScript", "level": 10},
        {"name": "SQL", "level": 11}
    ]
    
    # Sort or format them
    
    title_bar = f"""
    <rect width="100%" height="30" fill="{COLORS['border']}" rx="4" />
    <circle cx="15" cy="15" r="6" fill="#ff5f56"/>
    <circle cx="35" cy="15" r="6" fill="#ffbd2e"/>
    <circle cx="55" cy="15" r="6" fill="#27c93f"/>
    <text x="50%" y="20" class="text-primary" font-size="14" text-anchor="middle">yash@github: ~/skills</text>
    """
    
    bars = ""
    delay = 0.5
    for i, skill in enumerate(skills):
        name = skill["name"].ljust(12)
        bar = "█" * skill["level"]
        
        bars += f"""
        <g class="fade-in" style="animation-delay: {delay}s; opacity: 0;">
            <text x="30" y="{60 + i * 25}" font-size="14" class="text-accent" xml:space="preserve">{name}</text>
            <text x="140" y="{60 + i * 25}" font-size="14" class="text-primary bar-grow" style="animation-delay: {delay+0.2}s; clip-path: inset(0 100% 0 0);" xml:space="preserve">{bar}</text>
        </g>
        """
        delay += 0.2

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
    <style>
        .text-primary {{ font-family: {FONTS['primary']}; fill: {COLORS['primary']}; }}
        .text-secondary {{ font-family: {FONTS['primary']}; fill: {COLORS['secondary']}; }}
        .text-accent {{ font-family: {FONTS['primary']}; fill: {COLORS['accent']}; }}
        .bg {{ fill: {COLORS['background']}; }}
        .border {{ stroke: {COLORS['border']}; fill: none; }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateX(-10px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        .fade-in {{
            animation: fadeIn 0.4s forwards ease-out;
        }}
        
        @keyframes growBar {{
            from {{ clip-path: inset(0 100% 0 0); }}
            to {{ clip-path: inset(0 0 0 0); }}
        }}
        .bar-grow {{
            animation: growBar 0.6s forwards cubic-bezier(0.1, 0.8, 0.2, 1);
        }}
    </style>
    
    <rect width="400" height="300" class="bg" rx="6" />
    <rect width="400" height="300" class="border" rx="6" stroke-width="2"/>
    
    {title_bar}
    {bars}
</svg>"""

    save_svg("skills.svg", svg_content)

if __name__ == "__main__":
    generate_skills()
