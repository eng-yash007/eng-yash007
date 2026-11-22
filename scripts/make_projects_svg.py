"""
Generates the verified FEATURED.SYSTEMS card and individual interactive project cards for:
1. Silent Gallery
2. Guardian Transit AI
3. DocuDost
"""

from utils import FONTS, save_svg

def create_single_project_svg(p, filename):
    width = 280
    height = 210
    
    pills_svg = []
    p_x = 16
    for tech in p["stack"]:
        tw = len(tech) * 7.2 + 14
        pills_svg.append(f"""
        <rect x="{p_x}" y="146" width="{tw}" height="20" rx="4" fill="#1e293b" fill-opacity="0.8"/>
        <text x="{p_x + tw/2}" y="159.5" fill="#94a3b8" font-size="9.5" font-family="{FONTS['mono']}" text-anchor="middle">{tech}</text>
        """)
        p_x += tw + 6
    pills_markup = "".join(pills_svg)

    action_label = "OPEN LIVE APP ↗" if "LIVE" in p["badge"] else "VIEW ARCHITECTURE ↗"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="card-bg-{p['name'].replace(' ', '-').lower()}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0f172a" stop-opacity="0.96" />
            <stop offset="100%" stop-color="#060912" stop-opacity="0.96" />
        </linearGradient>
    </defs>

    <rect width="{width}" height="{height}" rx="12" fill="url(#card-bg-{p['name'].replace(' ', '-').lower()})" stroke="#1e293b" stroke-width="1.2"/>
    
    <!-- Status Badge -->
    <g transform="translate(16, 16)">
        <rect width="88" height="20" rx="4" fill="{p['badge_color']}" fill-opacity="0.15" stroke="{p['badge_color']}" stroke-width="1"/>
        <text x="44" y="14" fill="{p['badge_text']}" font-size="9.5" font-weight="700" font-family="{FONTS['mono']}" text-anchor="middle">{p['badge']}</text>
    </g>

    <!-- Action Prompt on top right -->
    <text x="{width - 16}" y="30" fill="{p['badge_text']}" font-size="10" font-weight="700" font-family="{FONTS['mono']}" text-anchor="end">{action_label}</text>
    
    <!-- Title -->
    <text x="16" y="56" fill="#f8fafc" font-size="16.5" font-weight="700" font-family="{FONTS['sans']}">{p['name']}</text>
    <text x="16" y="74" fill="#818cf8" font-size="11.5" font-weight="500" font-family="{FONTS['sans']}">{p['type']}</text>
    
    <!-- Description -->
    <text x="16" y="96" fill="#94a3b8" font-size="11.5" font-family="{FONTS['sans']}">
        <tspan x="16" dy="0">{p['desc1']}</tspan>
        <tspan x="16" dy="16">{p['desc2']}</tspan>
        <tspan x="16" dy="16">{p['desc3']}</tspan>
    </text>
    
    <!-- Tech Stack Pills -->
    {pills_markup}

    <!-- Bottom Action Ribbon -->
    <line x1="16" y1="178" x2="{width - 16}" y2="178" stroke="#1e293b" stroke-width="1" />
    <text x="{width / 2}" y="196" fill="#38bdf8" font-size="10.5" font-weight="600" font-family="{FONTS['mono']}" text-anchor="middle">⚡ Click card to launch project</text>
</svg>"""

    save_svg(filename, svg)

def generate_projects_svg():
    width = 900
    height = 250
    card_w = 265
    gap = 16
    start_x = 36
    start_y = 56
    card_h = 166

    projects = [
        {
            "name": "Silent Gallery",
            "type": "Voice AI Workspace",
            "badge": "LIVE DEMO",
            "badge_color": "#10b981",
            "badge_text": "#34d399",
            "desc1": "Voice productivity hub with Whisper",
            "desc2": "& Groq/Llama-3 for natural tasks,",
            "desc3": "and real-time Google Calendar sync.",
            "stack": ["Next.js", "Llama-3", "Whisper", "Supabase"],
            "url": "https://silent-galleryyy.vercel.app",
            "repo": "https://github.com/eng-yash007/silent_gallery",
            "file": "project_silent_gallery.svg"
        },
        {
            "name": "Guardian Transit AI",
            "type": "Biometric Transit Safety",
            "badge": "LIVE DEMO",
            "badge_color": "#3b82f6",
            "badge_text": "#60a5fa",
            "desc1": "Real-time CV pipeline using YOLOv8",
            "desc2": "& ArcFace for 512-d embeddings,",
            "desc3": "pgvector search & live telemetry.",
            "stack": ["FastAPI", "YOLOv8", "ArcFace", "pgvector"],
            "url": "https://guardian-transit-zeta.vercel.app",
            "repo": "https://github.com/eng-yash007/guardian-transit",
            "file": "project_guardian_transit.svg"
        },
        {
            "name": "DocuDost",
            "type": "Document RAG Intelligence",
            "badge": "ARCHITECTURE",
            "badge_color": "#8b5cf6",
            "badge_text": "#a78bfa",
            "desc1": "Enterprise multi-format RAG engine",
            "desc2": "with hybrid BM25 + dense FAISS,",
            "desc3": "cross-encoder reranking & citations.",
            "stack": ["Python", "FAISS", "LangChain", "FastAPI"],
            "url": "https://github.com/eng-yash007",
            "repo": "https://github.com/eng-yash007",
            "file": "project_docudost.svg"
        }
    ]

    # Generate individual cards
    for p in projects:
        create_single_project_svg(p, f"assets/{p['file']}")

    cards_svg = []
    for i, p in enumerate(projects):
        cx = start_x + i * (card_w + gap)
        
        pills_svg = []
        p_x = cx + 16
        for tech in p["stack"]:
            tw = len(tech) * 7.2 + 14
            pills_svg.append(f"""
            <rect x="{p_x}" y="{start_y + 128}" width="{tw}" height="20" rx="4" fill="#1e293b" fill-opacity="0.8"/>
            <text x="{p_x + tw/2}" y="{start_y + 141.5}" fill="#94a3b8" font-size="9.5" font-family="{FONTS['mono']}" text-anchor="middle">{tech}</text>
            """)
            p_x += tw + 6
        pills_markup = "".join(pills_svg)

        cards_svg.append(f"""
        <!-- Project {i+1}: {p['name']} -->
        <g class="project-card">
            <rect x="{cx}" y="{start_y}" width="{card_w}" height="{card_h}" rx="12" fill="#0b1120" stroke="#1e293b" stroke-width="1.2"/>
            
            <!-- Status Badge -->
            <g transform="translate({cx + 16}, {start_y + 16})">
                <rect width="84" height="20" rx="4" fill="{p['badge_color']}" fill-opacity="0.15" stroke="{p['badge_color']}" stroke-width="1"/>
                <text x="42" y="14" fill="{p['badge_text']}" font-size="9.5" font-weight="700" font-family="{FONTS['mono']}" text-anchor="middle">{p['badge']}</text>
            </g>
            
            <!-- Title -->
            <text x="{cx + 16}" y="{start_y + 54}" fill="#f8fafc" font-size="16" font-weight="700" font-family="{FONTS['sans']}">{p['name']}</text>
            <text x="{cx + 16}" y="{start_y + 71}" fill="#818cf8" font-size="11" font-weight="500" font-family="{FONTS['sans']}">{p['type']}</text>
            
            <!-- Description -->
            <text x="{cx + 16}" y="{start_y + 91}" fill="#94a3b8" font-size="11" font-family="{FONTS['sans']}">
                <tspan x="{cx + 16}" dy="0">{p['desc1']}</tspan>
                <tspan x="{cx + 16}" dy="16">{p['desc2']}</tspan>
                <tspan x="{cx + 16}" dy="16">{p['desc3']}</tspan>
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
