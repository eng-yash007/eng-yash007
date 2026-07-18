import json
from utils import COLORS, FONTS, save_svg

def generate_info_card():
    with open("data/profile.json", "r", encoding="utf-8") as f:
        profile = json.load(f)

    # Mac style title bar (red, yellow, green circles)
    title_bar = f"""
    <rect width="100%" height="30" fill="{COLORS['border']}" rx="4" />
    <circle cx="15" cy="15" r="6" fill="#ff5f56"/>
    <circle cx="35" cy="15" r="6" fill="#ffbd2e"/>
    <circle cx="55" cy="15" r="6" fill="#27c93f"/>
    <text x="50%" y="20" class="text-primary" font-size="14" text-anchor="middle">yash@github: ~</text>
    """

    # ASCII logo for Neofetch (Ubuntu)
    ubuntu_logo = f"""
    <g transform="translate(20, 50)" class="ubuntu-logo">
        <text class="text-accent" font-size="12">
            <tspan x="0" dy="1.2em">            .-/+oossssoo+/-.            </tspan>
            <tspan x="0" dy="1.2em">        `:+ssssssssssssssssss+:`        </tspan>
            <tspan x="0" dy="1.2em">      -+ssssssssssssssssssyyssss+-      </tspan>
            <tspan x="0" dy="1.2em">    .ossssssssssssssssssdMMMNysssso.    </tspan>
            <tspan x="0" dy="1.2em">   /ssssssssssshdmmNNmmyNMMMMhssssss/   </tspan>
            <tspan x="0" dy="1.2em">  +ssssssssshmydMMMMMMMNddddyssssssss+  </tspan>
            <tspan x="0" dy="1.2em"> /sssssssshNMMMyhhyyyyhmNMMMNhssssssss/ </tspan>
            <tspan x="0" dy="1.2em">.ssssssssdMMMNhsssssssssshNMMMdssssssss.</tspan>
            <tspan x="0" dy="1.2em">+sssssssyNMMMyssssssssssssyNMMMysssssss+</tspan>
            <tspan x="0" dy="1.2em">ossyhddddNMMMyssssssssssssyNMMMyddddyso</tspan>
            <tspan x="0" dy="1.2em">mNMMMMMMMMMMMyssssssssssssyNMMMMMMMMMMNm</tspan>
            <tspan x="0" dy="1.2em">ossyhddddNMMMyssssssssssssyNMMMyddddyso</tspan>
            <tspan x="0" dy="1.2em">+sssssssyNMMMyssssssssssssyNMMMysssssss+</tspan>
            <tspan x="0" dy="1.2em">.ssssssssdMMMNhsssssssssshNMMMdssssssss.</tspan>
            <tspan x="0" dy="1.2em"> /sssssssshNMMMyhhyyyyhdNMMMNhssssssss/ </tspan>
            <tspan x="0" dy="1.2em">  +sssssssssdmydMMMMMMMMddddyssssssss+  </tspan>
            <tspan x="0" dy="1.2em">   /ssssssssssshdmmNNmmyNMMMMhssssss/   </tspan>
            <tspan x="0" dy="1.2em">    .ossssssssssssssssssdMMMNysssso.    </tspan>
            <tspan x="0" dy="1.2em">      -+sssssssssssssssssyyyssss+-      </tspan>
            <tspan x="0" dy="1.2em">        `:+ssssssssssssssssss+:`        </tspan>
            <tspan x="0" dy="1.2em">            .-/+oossssoo+/-.            </tspan>
        </text>
    </g>
    """

    info_lines = [
        f"<tspan class='text-accent'>OS</tspan><tspan class='text-primary'>: Ubuntu</tspan>",
        f"<tspan class='text-accent'>Host</tspan><tspan class='text-primary'>: GitHub</tspan>",
        f"<tspan class='text-accent'>Name</tspan><tspan class='text-primary'>: {profile.get('name', 'Yash Gupta')}</tspan>",
        f"<tspan class='text-accent'>Role</tspan><tspan class='text-primary'>: {profile.get('role', 'AI Engineer')}</tspan>",
        f"<tspan class='text-accent'>College</tspan><tspan class='text-primary'>: {profile.get('college', 'ABES Engineering College')}</tspan>",
        f"<tspan class='text-accent'>Focus</tspan><tspan class='text-primary'>: {profile.get('focus', 'GenAI | Computer Vision')}</tspan>",
        f"<tspan class='text-accent'>Experience</tspan><tspan class='text-primary'>: {', '.join(profile.get('experience', []))}</tspan>",
        f"<tspan class='text-accent'>Learning</tspan><tspan class='text-primary'>: {profile.get('learning', 'System Design')}</tspan>",
        f"<tspan class='text-accent'>Status</tspan><tspan class='text-primary'>: {profile.get('status', 'Building AI Products 🚀')}</tspan>",
    ]

    info_texts = ""
    delay = 0.5
    for i, line in enumerate(info_lines):
        info_texts += f"""
        <g class="fade-in" style="animation-delay: {delay}s; opacity: 0;">
            <text x="320" y="{60 + i * 25}" font-size="14" class="text-primary">{line}</text>
        </g>
        """
        delay += 0.2

    # Add a blinking cursor at the end
    info_texts += f"""
    <g class="fade-in" style="animation-delay: {delay}s; opacity: 0;">
        <text x="320" y="{60 + len(info_lines) * 25}" font-size="14" class="text-accent prompt">yash@github:~$ <tspan class="blink">_</tspan></text>
    </g>
    """

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="350" viewBox="0 0 800 350">
    <style>
        .text-primary {{ font-family: {FONTS['primary']}; fill: {COLORS['primary']}; }}
        .text-secondary {{ font-family: {FONTS['primary']}; fill: {COLORS['secondary']}; }}
        .text-accent {{ font-family: {FONTS['primary']}; fill: {COLORS['accent']}; }}
        .bg {{ fill: {COLORS['background']}; }}
        .border {{ stroke: {COLORS['border']}; fill: none; }}
        
        @keyframes fadeInSlide {{
            0% {{ opacity: 0; transform: translateX(-10px); }}
            100% {{ opacity: 1; transform: translateX(0); }}
        }}
        .fade-in {{
            animation: fadeInSlide 0.5s forwards ease-out;
        }}
        
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0; }}
        }}
        .blink {{
            animation: blink 1s step-end infinite;
        }}
        
        @keyframes slideInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .ubuntu-logo {{
            animation: slideInUp 0.8s forwards ease-out;
            opacity: 0;
        }}
    </style>
    
    <rect width="800" height="350" class="bg" rx="6" />
    <rect width="800" height="350" class="border" rx="6" stroke-width="2"/>
    
    {title_bar}
    {ubuntu_logo}
    {info_texts}
    
</svg>"""

    save_svg("info-card.svg", svg_content)

if __name__ == "__main__":
    generate_info_card()