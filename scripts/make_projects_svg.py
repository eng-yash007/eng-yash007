"""
Generates the verified FEATURED.SYSTEMS dashboard card (900x270) for:
1. SILENT GALLERY (Voice AI & Smart Task Workspace)
2. GUARDIAN TRANSIT AI (Computer Vision & Student Safety)
Engineered strictly following the Premium Dark Tech Design System.
"""

from utils import THEME, FONTS, escape, save_svg

def generate_projects_svg():
    width = 900
    height = 270
    card_w = 404
    gap = 20
    start_x = 36
    start_y = 60
    card_h = 186

    projects = [
        {
            "id": "SYS-01",
            "name": "SILENT GALLERY",
            "type": "Voice AI & Smart Task Workspace",
            "badge": "LIVE PRODUCTION",
            "badge_color": "#10B981",
            "badge_text": "#34D399",
            "accent": THEME["violet"],
            "desc1": "Voice productivity hub with Whisper & Groq/Llama-3 for",
            "desc2": "hands-free task execution and automated Google Calendar scheduling.",
            "stack": ["Next.js", "Llama-3", "Whisper", "Supabase", "FastAPI"],
            "url": "https://silent-galleryyy.vercel.app",
            "repo": "https://github.com/eng-yash007/silent_gallery"
        },
        {
            "id": "SYS-02",
            "name": "GUARDIAN TRANSIT AI",
            "type": "Computer Vision & Student Safety",
            "badge": "LIVE PRODUCTION",
            "badge_color": "#3B82F6",
            "badge_text": "#60A5FA",
            "accent": THEME["electric_blue"],
            "desc1": "Real-time CV pipeline using YOLOv8 & ArcFace 512-d embeddings,",
            "desc2": "sub-50ms pgvector similarity search & live transit telemetry.",
            "stack": ["FastAPI", "YOLOv8", "ArcFace", "pgvector", "Python"],
            "url": "https://guardian-transit-zeta.vercel.app",
            "repo": "https://github.com/eng-yash007/guardian-transit"
        }
    ]

    cards_svg = []
    for i, p in enumerate(projects):
        cx = start_x + i * (card_w + gap)
        
        # Calculate tech stack pills with safe widths
        pills_svg = []
        p_x = cx + 20
        for tech in p["stack"]:
            tw = len(tech) * 7.5 + 16
            pills_svg.append(f"""
            <rect x="{p_x}" y="{start_y + 118}" width="{tw}" height="22" rx="4" fill="#0D1424" stroke="#1E293B" stroke-width="1"/>
            <text x="{p_x + tw/2}" y="{start_y + 133}" fill="#94A3B8" font-size="10.5" font-family="{FONTS['mono']}" text-anchor="middle">{tech}</text>
            """)
            p_x += tw + 7
        pills_markup = "".join(pills_svg)

        cards_svg.append(f"""
        <!-- Card {i+1}: {p['name']} -->
        <g class="project-card">
            <!-- Card Outer Surface -->
            <rect x="{cx}" y="{start_y}" width="{card_w}" height="{card_h}" rx="12" fill="#0B1120" stroke="#1E293B" stroke-width="1.2"/>
            
            <!-- Subtle accent border glow -->
            <rect x="{cx}" y="{start_y}" width="{card_w}" height="{card_h}" rx="12" fill="none" stroke="{p['accent']}" stroke-width="1" stroke-opacity="0.3"/>
            
            <!-- Top Status Bar: Identifier & Badge -->
            <g transform="translate({cx + 20}, {start_y + 18})">
                <text x="0" y="14" fill="#64748B" font-size="10" font-weight="700" font-family="{FONTS['mono']}">{p['id']}</text>
                
                <rect x="56" y="0" width="116" height="20" rx="4" fill="{p['badge_color']}" fill-opacity="0.12" stroke="{p['badge_color']}" stroke-width="1"/>
                <circle cx="66" cy="10" r="3" fill="{p['badge_text']}" />
                <text x="116" y="14" fill="{p['badge_text']}" font-size="9" font-weight="700" font-family="{FONTS['mono']}" text-anchor="middle">{p['badge']}</text>
            </g>

            <!-- Action Prompt -->
            <text x="{cx + card_w - 20}" y="{start_y + 32}" fill="{p['accent']}" font-size="10.5" font-weight="700" font-family="{FONTS['mono']}" text-anchor="end">VERIFIED ↗</text>
            
            <!-- Title & Subtitle -->
            <text x="{cx + 20}" y="{start_y + 60}" fill="#F1F5F9" font-size="17" font-weight="800" font-family="{FONTS['sans']}">{escape(p['name'])}</text>
            <text x="{cx + 20}" y="{start_y + 78}" fill="{p['accent']}" font-size="11.5" font-weight="600" font-family="{FONTS['sans']}">{escape(p['type'])}</text>
            
            <!-- Description -->
            <text x="{cx + 20}" y="{start_y + 96}" fill="#94A3B8" font-size="11" font-family="{FONTS['sans']}">
                <tspan x="{cx + 20}" dy="0">{escape(p['desc1'])}</tspan>
                <tspan x="{cx + 20}" dy="15">{escape(p['desc2'])}</tspan>
            </text>
            
            <!-- Tech Stack Pills -->
            {pills_markup}

            <!-- Card Bottom Ribbon: Direct Action Guides -->
            <line x1="{cx + 20}" y1="{start_y + 152}" x2="{cx + card_w - 20}" y2="{start_y + 152}" stroke="#1E293B" stroke-width="1" />
            <g transform="translate({cx + 20}, {start_y + 168})">
                <circle cx="4" cy="-3" r="2.5" fill="#38BDF8" />
                <text x="14" y="0" fill="#38BDF8" font-size="10" font-weight="600" font-family="{FONTS['mono']}">Live Demo</text>
                <text x="80" y="0" fill="#64748B" font-size="10" font-family="{FONTS['mono']}">|</text>
                <circle cx="96" cy="-3" r="2.5" fill="#8B5CF6" />
                <text x="106" y="0" fill="#8B5CF6" font-size="10" font-weight="600" font-family="{FONTS['mono']}">GitHub Repo</text>
                <text x="{card_w - 40}" y="0" fill="#64748B" font-size="9.5" font-family="{FONTS['mono']}" text-anchor="end">Click links below ↓</text>
            </g>
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
    <g transform="translate(36, 30)">
        <path d="M 0 14 L 0 0 L 14 0" fill="none" stroke="#38BDF8" stroke-width="2"/>
        <text x="22" y="10" fill="#38BDF8" font-size="12" font-weight="700" font-family="{FONTS['mono']}">FEATURED.SYSTEMS</text>
        <circle cx="180" cy="6" r="3.5" fill="#34D399"/>
        <text x="192" y="10" fill="#64748B" font-size="10.5" font-family="{FONTS['mono']}">PRODUCTION DEPLOYMENTS</text>
    </g>

    {all_cards}
</svg>"""

    save_svg("projects.svg", svg)

if __name__ == "__main__":
    generate_projects_svg()
