"""
Generates the minimal, modern, verified FEATURED.SYSTEMS dashboard SVG (900x280).
Strictly adheres to the Premium Dark Tech Design System:
- Project 01: Silent Gallery (Voice AI & Smart Task Workspace)
- Project 02: Guardian Transit AI (Computer Vision & Student Safety)
- Each card contains small project identifier, title, category, concise description,
  compact tech tags, and TWO embedded actions inside the card:
  1. Live Demo (direct working link)
  2. GitHub Repository (direct working link)
- Zero separate link rows below the cards.
"""

from utils import THEME, FONTS, escape, save_svg

def generate_projects_svg():
    width = 900
    height = 280
    card_w = 404
    card_h = 204
    gap = 20
    start_x = 36
    start_y = 54

    projects = [
        {
            "num": "PROJECT 01",
            "name": "Silent Gallery",
            "category": "Voice AI & Smart Task Workspace",
            "accent": THEME["cyan"],
            "btn_accent": THEME["electric_blue"],
            "desc1": "AI-powered productivity workspace with voice interaction",
            "desc2": "and hands-free task automation.",
            "stack": ["Next.js", "Llama-3", "Whisper", "Supabase", "FastAPI"],
            "url": "https://silent-galleryyy.vercel.app",
            "repo": "https://github.com/eng-yash007/silent_gallery"
        },
        {
            "num": "PROJECT 02",
            "name": "Guardian Transit AI",
            "category": "Computer Vision & Student Safety",
            "accent": THEME["violet"],
            "btn_accent": THEME["violet"],
            "desc1": "AI-powered transit safety system using computer vision",
            "desc2": "and real-time student monitoring.",
            "stack": ["FastAPI", "YOLOv8", "ArcFace", "pgvector", "Python"],
            "url": "https://guardian-transit-zeta.vercel.app",
            "repo": "https://github.com/eng-yash007/guardian-transit"
        }
    ]

    cards_svg = []
    for i, p in enumerate(projects):
        cx = start_x + i * (card_w + gap)

        # Tech stack pills
        pills_svg = []
        p_x = cx + 20
        for tech in p["stack"]:
            tw = len(tech) * 7.2 + 14
            pills_svg.append(f"""
            <rect x="{p_x}" y="{start_y + 116}" width="{tw:.1f}" height="20" rx="4" fill="#0D1424" stroke="#1E293B" stroke-width="1"/>
            <text x="{p_x + tw/2.0:.1f}" y="{start_y + 130}" fill="#94A3B8" font-size="10" font-family="{FONTS['mono']}" text-anchor="middle">{escape(tech)}</text>
            """)
            p_x += tw + 6
        pills_markup = "".join(pills_svg)

        btn1_x = cx + 20
        btn1_w = 176
        btn2_x = cx + 208
        btn2_w = 176
        btn_y = start_y + 162
        btn_h = 28

        cards_svg.append(f"""
        <!-- Card {i+1}: {escape(p['name'])} -->
        <g class="project-card">
            <!-- Card Outer Surface -->
            <rect x="{cx}" y="{start_y}" width="{card_w}" height="{card_h}" rx="10" fill="#0B1120" stroke="#1E293B" stroke-width="1.1"/>
            
            <!-- Subtle accent top border -->
            <line x1="{cx + 12}" y1="{start_y}" x2="{cx + card_w - 12}" y2="{start_y}" stroke="{p['accent']}" stroke-opacity="0.5" stroke-width="1"/>

            <!-- Header Row: Project Identifier & Category -->
            <text x="{cx + 20}" y="{start_y + 24}" fill="#64748B" font-size="10.5" font-weight="700" font-family="{FONTS['mono']}">{p['num']}</text>
            <text x="{cx + card_w - 20}" y="{start_y + 24}" fill="{p['accent']}" font-size="11" font-weight="600" font-family="{FONTS['sans']}" text-anchor="end">{escape(p['category'])}</text>

            <!-- Title -->
            <text x="{cx + 20}" y="{start_y + 54}" fill="#F1F5F9" font-size="17" font-weight="700" font-family="{FONTS['sans']}">{escape(p['name'])}</text>

            <!-- Concise Description -->
            <text x="{cx + 20}" y="{start_y + 76}" fill="#94A3B8" font-size="11.5" font-family="{FONTS['sans']}">
                <tspan x="{cx + 20}" dy="0">{escape(p['desc1'])}</tspan>
                <tspan x="{cx + 20}" dy="16">{escape(p['desc2'])}</tspan>
            </text>

            <!-- Tech Tags -->
            {pills_markup}

            <!-- Divider -->
            <line x1="{cx + 20}" y1="{start_y + 150}" x2="{cx + card_w - 20}" y2="{start_y + 150}" stroke="#1E293B" stroke-width="1" />

            <!-- Action 1: Live Demo (Inside Card) -->
            <a href="{p['url']}" xlink:href="{p['url']}" target="_blank" class="action-btn">
                <rect x="{btn1_x}" y="{btn_y}" width="{btn1_w}" height="{btn_h}" rx="6" fill="#0D1424" stroke="#38BDF8" stroke-opacity="0.8" stroke-width="1"/>
                <text x="{btn1_x + btn1_w/2.0}" y="{btn_y + 18}" fill="#38BDF8" font-size="11" font-weight="600" font-family="{FONTS['mono']}" text-anchor="middle">Live Demo ↗</text>
            </a>

            <!-- Action 2: GitHub Repository (Inside Card) -->
            <a href="{p['repo']}" xlink:href="{p['repo']}" target="_blank" class="action-btn">
                <rect x="{btn2_x}" y="{btn_y}" width="{btn2_w}" height="{btn_h}" rx="6" fill="#0D1424" stroke="#8B5CF6" stroke-opacity="0.8" stroke-width="1"/>
                <text x="{btn2_x + btn2_w/2.0}" y="{btn_y + 18}" fill="#8B5CF6" font-size="11" font-weight="600" font-family="{FONTS['mono']}" text-anchor="middle">GitHub Repo ↗</text>
            </a>
        </g>
        """)

    all_cards = "".join(cards_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="proj-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#080D18" />
            <stop offset="50%" stop-color="#0D1424" />
            <stop offset="100%" stop-color="#080D18" />
        </linearGradient>

        <linearGradient id="proj-border" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1E293B" stop-opacity="0.9"/>
            <stop offset="50%" stop-color="#334155" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#1E293B" stop-opacity="0.9"/>
        </linearGradient>
    </defs>

    <style>
        .font-sans {{ font-family: {FONTS['sans']}; }}
        .font-mono {{ font-family: {FONTS['mono']}; }}

        .action-btn {{
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .action-btn:hover rect {{
            fill: #162036;
            stroke-opacity: 1;
        }}
    </style>

    <!-- Outer Container -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#proj-bg)" stroke="url(#proj-border)" stroke-width="1.2"/>
    
    <!-- Header -->
    <g transform="translate(36, 30)">
        <path d="M 0 14 L 0 0 L 14 0" fill="none" stroke="#38BDF8" stroke-width="2"/>
        <text x="22" y="10" fill="#38BDF8" font-size="12" font-weight="700" class="font-mono">FEATURED.SYSTEMS</text>
        <circle cx="180" cy="6" r="3.5" fill="#34D399"/>
        <text x="192" y="10" fill="#64748B" font-size="10.5" class="font-mono">PRODUCTION DEPLOYMENTS</text>
    </g>

    {all_cards}
</svg>"""

    save_svg("projects.svg", svg)

if __name__ == "__main__":
    generate_projects_svg()
