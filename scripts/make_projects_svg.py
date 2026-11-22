"""
Generates the verified FEATURED.SYSTEMS dashboard card (900x260) for:
1. Silent Gallery
2. Guardian Transit AI
Built from scratch with zero fragile table dependencies.
"""

from utils import FONTS, save_svg

def generate_projects_svg():
    width = 900
    height = 260
    card_w = 404
    gap = 20
    start_x = 36
    start_y = 60
    card_h = 176

    projects = [
        {
            "name": "Silent Gallery",
            "type": "Voice AI & Smart Task Workspace",
            "badge": "LIVE PRODUCTION",
            "badge_color": "#10b981",
            "badge_text": "#34d399",
            "desc1": "Voice productivity hub with Whisper & Groq/Llama-3 for",
            "desc2": "hands-free task execution and automated Google Calendar scheduling.",
            "stack": ["Next.js", "Llama-3", "Whisper", "Supabase", "FastAPI"],
            "url": "https://silent-galleryyy.vercel.app",
            "repo": "https://github.com/eng-yash007/silent_gallery"
        },
        {
            "name": "Guardian Transit AI",
            "type": "Edge AI & Biometric Public Transit Safety",
            "badge": "LIVE PRODUCTION",
            "badge_color": "#3b82f6",
            "badge_text": "#60a5fa",
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
        
        pills_svg = []
        p_x = cx + 20
        for tech in p["stack"]:
            tw = len(tech) * 7.5 + 16
            pills_svg.append(f"""
            <rect x="{p_x}" y="{start_y + 132}" width="{tw}" height="22" rx="4" fill="#1e293b" fill-opacity="0.85" stroke="#334155" stroke-width="0.8"/>
            <text x="{p_x + tw/2}" y="{start_y + 147}" fill="#cbd5e1" font-size="10.5" font-family="{FONTS['mono']}" text-anchor="middle">{tech}</text>
            """)
            p_x += tw + 8
        pills_markup = "".join(pills_svg)

        cards_svg.append(f"""
        <!-- Card {i+1}: {p['name']} -->
        <g class="project-card">
            <rect x="{cx}" y="{start_y}" width="{card_w}" height="{card_h}" rx="14" fill="#0b1120" stroke="#1e293b" stroke-width="1.2"/>
            
            <!-- Status Badge -->
            <g transform="translate({cx + 20}, {start_y + 18})">
                <rect width="124" height="22" rx="4" fill="{p['badge_color']}" fill-opacity="0.15" stroke="{p['badge_color']}" stroke-width="1"/>
                <circle cx="12" cy="11" r="3.5" fill="{p['badge_text']}" />
                <text x="68" y="15" fill="{p['badge_text']}" font-size="9.5" font-weight="700" font-family="{FONTS['mono']}" text-anchor="middle">{p['badge']}</text>
            </g>

            <!-- Action Prompt -->
            <text x="{cx + card_w - 20}" y="{start_y + 33}" fill="{p['badge_text']}" font-size="11" font-weight="700" font-family="{FONTS['mono']}" text-anchor="end">LAUNCH APP ↗</text>
            
            <!-- Title & Subtitle -->
            <text x="{cx + 20}" y="{start_y + 64}" fill="#f8fafc" font-size="19" font-weight="700" font-family="{FONTS['sans']}">{p['name']}</text>
            <text x="{cx + 20}" y="{start_y + 84}" fill="#818cf8" font-size="12" font-weight="500" font-family="{FONTS['sans']}">{p['type']}</text>
            
            <!-- Description -->
            <text x="{cx + 20}" y="{start_y + 104}" fill="#94a3b8" font-size="11.5" font-family="{FONTS['sans']}">
                <tspan x="{cx + 20}" dy="0">{p['desc1']}</tspan>
                <tspan x="{cx + 20}" dy="16">{p['desc2']}</tspan>
            </text>
            
            <!-- Tech Stack Pills -->
            {pills_markup}
        </g>
        """)

    all_cards = "".join(cards_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="proj-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#080c16" />
            <stop offset="50%" stop-color="#0b101d" />
            <stop offset="100%" stop-color="#050811" />
        </linearGradient>

        <linearGradient id="proj-border" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1e293b" stop-opacity="0.9"/>
            <stop offset="50%" stop-color="#334155" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#1e293b" stop-opacity="0.9"/>
        </linearGradient>
    </defs>

    <!-- Outer Container -->
    <rect width="{width}" height="{height}" rx="16" fill="url(#proj-bg)" stroke="url(#proj-border)" stroke-width="1.2"/>
    
    <!-- Header -->
    <g transform="translate(36, 32)">
        <path d="M 0 14 L 0 0 L 14 0" fill="none" stroke="#38bdf8" stroke-width="2"/>
        <text x="22" y="10" fill="#38bdf8" font-size="12.5" font-weight="700" font-family="{FONTS['mono']}">FEATURED.SYSTEMS</text>
        <circle cx="185" cy="6" r="3.5" fill="#34d399"/>
        <text x="196" y="10" fill="#64748b" font-size="11" font-family="{FONTS['mono']}">PRODUCTION DEPLOYMENTS</text>
    </g>

    {all_cards}
</svg>"""

    save_svg("projects.svg", svg)

if __name__ == "__main__":
    generate_projects_svg()
