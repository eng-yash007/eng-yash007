"""
Generates the verified FEATURED.SYSTEMS cards for:
1. Silent Gallery
2. Guardian Transit AI
(DocuDost removed per user request, strictly focusing on the 2 top live production systems)
"""

from utils import FONTS, save_svg

def create_single_project_svg(p, filename):
    width = 440
    height = 220
    
    pills_svg = []
    p_x = 20
    for tech in p["stack"]:
        tw = len(tech) * 7.5 + 16
        pills_svg.append(f"""
        <rect x="{p_x}" y="152" width="{tw}" height="22" rx="5" fill="#1e293b" fill-opacity="0.85" stroke="#334155" stroke-width="0.8"/>
        <text x="{p_x + tw/2}" y="167" fill="#cbd5e1" font-size="10.5" font-family="{FONTS['mono']}" text-anchor="middle">{tech}</text>
        """)
        p_x += tw + 8
    pills_markup = "".join(pills_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="card-bg-{p['key']}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0e1628" stop-opacity="0.96" />
            <stop offset="100%" stop-color="#070a14" stop-opacity="0.96" />
        </linearGradient>

        <linearGradient id="glow-{p['key']}" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{p['badge_color']}" stop-opacity="0.6" />
            <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.3" />
        </linearGradient>
    </defs>

    <!-- Outer Card Frame -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#card-bg-{p['key']})" stroke="#1e293b" stroke-width="1.2"/>
    <rect width="{width}" height="{height}" rx="14" fill="none" stroke="url(#glow-{p['key']})" stroke-width="1" />
    
    <!-- Status Badge -->
    <g transform="translate(20, 18)">
        <rect width="108" height="22" rx="4" fill="{p['badge_color']}" fill-opacity="0.15" stroke="{p['badge_color']}" stroke-width="1.1"/>
        <circle cx="12" cy="11" r="3.5" fill="{p['badge_text']}" />
        <text x="58" y="15" fill="{p['badge_text']}" font-size="10" font-weight="700" font-family="{FONTS['mono']}" text-anchor="middle">{p['badge']}</text>
    </g>

    <!-- Action Prompt on top right -->
    <text x="{width - 20}" y="33" fill="{p['badge_text']}" font-size="11" font-weight="700" font-family="{FONTS['mono']}" text-anchor="end">LAUNCH APP ↗</text>
    
    <!-- Title & Subtitle -->
    <text x="20" y="66" fill="#f8fafc" font-size="19" font-weight="700" font-family="{FONTS['sans']}">{p['name']}</text>
    <text x="20" y="86" fill="#818cf8" font-size="12" font-weight="500" font-family="{FONTS['sans']}">{p['type']}</text>
    
    <!-- Description -->
    <text x="20" y="110" fill="#94a3b8" font-size="12" font-family="{FONTS['sans']}">
        <tspan x="20" dy="0">{p['desc1']}</tspan>
        <tspan x="20" dy="18">{p['desc2']}</tspan>
    </text>
    
    <!-- Tech Stack Pills -->
    {pills_markup}

    <!-- Bottom Action Ribbon -->
    <line x1="20" y1="188" x2="{width - 20}" y2="188" stroke="#1e293b" stroke-width="1" />
    <text x="{width / 2}" y="206" fill="#38bdf8" font-size="11" font-weight="600" font-family="{FONTS['mono']}" text-anchor="middle">⚡ Click card to open live deployment</text>
</svg>"""

    save_svg(filename, svg)

def generate_projects_svg():
    width = 900
    height = 250
    card_w = 406
    gap = 16
    start_x = 36
    start_y = 56
    card_h = 168

    projects = [
        {
            "key": "silent-gallery",
            "name": "Silent Gallery",
            "type": "Voice AI & Task Automation Workspace",
            "badge": "LIVE APP",
            "badge_color": "#10b981",
            "badge_text": "#34d399",
            "desc1": "Voice productivity hub with Whisper & Groq/Llama-3 for hands-free tasks.",
            "desc2": "Real-time task execution, voice synthesis & Google Calendar synchronization.",
            "stack": ["Next.js", "Llama-3", "Whisper", "Supabase", "FastAPI"],
            "url": "https://silent-galleryyy.vercel.app",
            "repo": "https://github.com/eng-yash007/silent_gallery",
            "file": "project_silent_gallery.svg"
        },
        {
            "key": "guardian-transit",
            "name": "Guardian Transit AI",
            "type": "Edge AI & Biometric Public Transit Security",
            "badge": "LIVE APP",
            "badge_color": "#3b82f6",
            "badge_text": "#60a5fa",
            "desc1": "Real-time CV pipeline using YOLOv8 & ArcFace for 512-d biometric embeddings.",
            "desc2": "Sub-50ms pgvector similarity search, multi-camera tracking & live alerts.",
            "stack": ["FastAPI", "YOLOv8", "ArcFace", "pgvector", "Python"],
            "url": "https://guardian-transit-zeta.vercel.app",
            "repo": "https://github.com/eng-yash007/guardian-transit",
            "file": "project_guardian_transit.svg"
        }
    ]

    # Generate individual cards (440x220)
    for p in projects:
        create_single_project_svg(p, f"assets/{p['file']}")

    cards_svg = []
    for i, p in enumerate(projects):
        cx = start_x + i * (card_w + gap)
        
        pills_svg = []
        p_x = cx + 20
        for tech in p["stack"]:
            tw = len(tech) * 7.5 + 14
            pills_svg.append(f"""
            <rect x="{p_x}" y="{start_y + 128}" width="{tw}" height="20" rx="4" fill="#1e293b" fill-opacity="0.85"/>
            <text x="{p_x + tw/2}" y="{start_y + 142}" fill="#cbd5e1" font-size="10" font-family="{FONTS['mono']}" text-anchor="middle">{tech}</text>
            """)
            p_x += tw + 8
        pills_markup = "".join(pills_svg)

        cards_svg.append(f"""
        <!-- Project {i+1}: {p['name']} -->
        <g class="project-card">
            <rect x="{cx}" y="{start_y}" width="{card_w}" height="{card_h}" rx="12" fill="#0b1120" stroke="#1e293b" stroke-width="1.2"/>
            
            <!-- Status Badge -->
            <g transform="translate({cx + 18}, {start_y + 16})">
                <rect width="90" height="20" rx="4" fill="{p['badge_color']}" fill-opacity="0.15" stroke="{p['badge_color']}" stroke-width="1"/>
                <circle cx="10" cy="10" r="3" fill="{p['badge_text']}" />
                <text x="50" y="14" fill="{p['badge_text']}" font-size="9.5" font-weight="700" font-family="{FONTS['mono']}" text-anchor="middle">{p['badge']}</text>
            </g>

            <text x="{cx + card_w - 18}" y="{start_y + 30}" fill="{p['badge_text']}" font-size="10" font-weight="700" font-family="{FONTS['mono']}" text-anchor="end">OPEN APP ↗</text>
            
            <!-- Title -->
            <text x="{cx + 18}" y="{start_y + 54}" fill="#f8fafc" font-size="17" font-weight="700" font-family="{FONTS['sans']}">{p['name']}</text>
            <text x="{cx + 18}" y="{start_y + 72}" fill="#818cf8" font-size="11.5" font-weight="500" font-family="{FONTS['sans']}">{p['type']}</text>
            
            <!-- Description -->
            <text x="{cx + 18}" y="{start_y + 92}" fill="#94a3b8" font-size="11" font-family="{FONTS['sans']}">
                <tspan x="{cx + 18}" dy="0">{p['desc1']}</tspan>
                <tspan x="{cx + 18}" dy="16">{p['desc2']}</tspan>
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
            <stop offset="100%" stop-color="#050811" />
        </linearGradient>
    </defs>

    <!-- Outer Container -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#proj-bg)" stroke="#1e293b" stroke-width="1.2"/>
    
    <!-- Header -->
    <g transform="translate(36, 28)">
        <path d="M 0 14 L 0 0 L 14 0" fill="none" stroke="#38bdf8" stroke-width="2"/>
        <text x="22" y="10" fill="#38bdf8" font-size="13" font-weight="700" font-family="{FONTS['mono']}">FEATURED.SYSTEMS</text>
        <circle cx="185" cy="6" r="3.5" fill="#34d399"/>
        <text x="196" y="10" fill="#64748b" font-size="11" font-family="{FONTS['mono']}">PRODUCTION DEPLOYMENTS</text>
    </g>

    {all_cards}
</svg>"""

    save_svg("assets/projects.svg", svg)

if __name__ == "__main__":
    generate_projects_svg()
