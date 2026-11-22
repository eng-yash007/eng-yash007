"""
Generates the verified FEATURED.SYSTEMS dashboard card (900x240) for:
1. Silent Gallery: Voice AI & Smart Task Workspace
2. Guardian Transit AI: Computer Vision & Student Safety
Strictly well-formed XML with zero unescaped tokens.
"""

from utils import THEME, FONTS, escape, save_svg

def generate_projects_svg():
    width = 900
    height = 240
    card_w = 412
    gap = 20
    start_x = 28
    start_y = 54
    card_h = 162

    projects = [
        {
            "id": "PROJECT.01 // PRODUCTION",
            "name": "Silent Gallery",
            "type": "Voice AI & Smart Task Workspace",
            "badge_color": "#10B981",
            "badge_glow": "#34D399",
            "desc": "Voice-enabled smart workspace with Whisper, Llama-3 & Google Calendar sync.",
            "stack": ["Next.js", "Llama-3", "Whisper", "Supabase", "FastAPI"],
            "live_url": "https://silent-galleryyy.vercel.app",
            "repo_url": "https://github.com/eng-yash007/silent_gallery"
        },
        {
            "id": "PROJECT.02 // PRODUCTION",
            "name": "Guardian Transit AI",
            "type": "Computer Vision & Student Safety",
            "badge_color": "#38BDF8",
            "badge_glow": "#22D3EE",
            "desc": "Biometric student transit safety with YOLOv8, ArcFace & pgvector similarity search.",
            "stack": ["FastAPI", "YOLOv8", "ArcFace", "pgvector", "Docker"],
            "live_url": "https://guardian-transit-zeta.vercel.app",
            "repo_url": "https://github.com/eng-yash007/guardian-transit"
        }
    ]

    cards_svg = []
    for i, p in enumerate(projects):
        cx = start_x + i * (card_w + gap)
        
        # Tech Stack Pills
        pills_svg = []
        p_x = cx + 18
        for tech in p["stack"]:
            tw = len(tech) * 7.2 + 14
            pills_svg.append(f"""
            <rect x="{p_x}" y="{start_y + 122}" width="{tw}" height="20" rx="4" fill="#0D1424" stroke="#1E293B" stroke-width="0.9"/>
            <text x="{p_x + tw/2}" y="{start_y + 135.5}" fill="#94A3B8" font-size="9.5" font-family="{FONTS['mono']}" text-anchor="middle">{escape(tech)}</text>
            """)
            p_x += tw + 6
        pills_markup = "".join(pills_svg)

        cards_svg.append(f"""
        <!-- Card {i+1}: {escape(p['name'])} -->
        <g class="project-card">
            <!-- Card Container -->
            <rect x="{cx}" y="{start_y}" width="{card_w}" height="{card_h}" rx="12" fill="#0B1120" stroke="#1E293B" stroke-width="1.1"/>
            
            <!-- Header Tag & Identifier -->
            <g transform="translate({cx + 18}, {start_y + 16})">
                <circle cx="4" cy="6" r="3.5" fill="{p['badge_glow']}" />
                <text x="14" y="9.5" fill="{p['badge_glow']}" font-size="9.5" font-weight="700" font-family="{FONTS['mono']}">{escape(p['id'])}</text>
            </g>

            <!-- Action Prompt -->
            <text x="{cx + card_w - 18}" y="{start_y + 25.5}" fill="#38BDF8" font-size="10.5" font-weight="600" font-family="{FONTS['mono']}" text-anchor="end">Live App ↗</text>
            
            <!-- Title & Subtitle -->
            <text x="{cx + 18}" y="{start_y + 54}" fill="#F1F5F9" font-size="18" font-weight="700" font-family="{FONTS['sans']}">{escape(p['name'])}</text>
            <text x="{cx + 18}" y="{start_y + 72}" fill="#8B5CF6" font-size="11.5" font-weight="500" font-family="{FONTS['sans']}">{escape(p['type'])}</text>
            
            <!-- One-Line Description -->
            <text x="{cx + 18}" y="{start_y + 95}" fill="#94A3B8" font-size="11.5" font-family="{FONTS['sans']}">
                {escape(p['desc'])}
            </text>
            
            <!-- Tech Stack Pills -->
            {pills_markup}
        </g>
        """)

    all_cards = "".join(cards_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
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

    <!-- Outer Container -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#proj-bg)" stroke="url(#proj-border)" stroke-width="1.2"/>
    
    <!-- Header -->
    <g transform="translate(28, 28)">
        <path d="M 0 14 L 0 0 L 14 0" fill="none" stroke="#38BDF8" stroke-width="2"/>
        <text x="22" y="10" fill="#38BDF8" font-size="12" font-weight="700" font-family="{FONTS['mono']}">FEATURED.SYSTEMS</text>
        <circle cx="170" cy="6" r="3.5" fill="#22D3EE"/>
        <text x="182" y="10" fill="#94A3B8" font-size="10.5" font-family="{FONTS['mono']}">PRODUCTION DEPLOYMENTS</text>
    </g>

    {all_cards}
</svg>"""

    save_svg("projects.svg", svg)

if __name__ == "__main__":
    generate_projects_svg()
