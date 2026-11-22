"""
Generates the verified FEATURED.SYSTEMS card for the 3 strongest projects:
Silent Gallery, Guardian Transit AI, DocuDost.
"""

from utils import FONTS, save_svg

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
            "repo": "github.com/eng-yash007/silent_gallery"
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
            "repo": "github.com/eng-yash007/guardian-transit"
        },
        {
            "name": "DocuDost",
            "type": "Document RAG Intelligence",
            "badge": "ARCHITECTURE",
            "badge_color": "#8b5cf6",
            "badge_text": "#c084fc",
            "desc1": "Enterprise document intelligence",
            "desc2": "platform powered by LangChain RAG,",
            "desc3": "FAISS vector store, and Hugging Face.",
            "stack": ["Python", "LangChain", "RAG", "FAISS"],
            "repo": "github.com/eng-yash007"
        }
    ]

    cards_svg = []
    for idx, p in enumerate(projects):
        x = start_x + idx * (card_w + gap)
        
        # Tech pills
        pills_svg = []
        p_x = 16
        for tech in p["stack"]:
            tw = len(tech) * 7.2 + 14
            pills_svg.append(f"""
            <rect x="{p_x}" y="128" width="{tw}" height="18" rx="4" fill="#1e293b" fill-opacity="0.8"/>
            <text x="{p_x + tw/2}" y="140.5" fill="#94a3b8" font-size="9.5" font-family="{FONTS['mono']}" text-anchor="middle">{tech}</text>
            """)
            p_x += tw + 6
        pills_markup = "".join(pills_svg)

        cards_svg.append(f"""
        <g transform="translate({x}, {start_y})">
            <rect width="{card_w}" height="{card_h}" rx="10" fill="#0f172a" fill-opacity="0.9" stroke="#1e293b" stroke-width="1.1"/>
            
            <!-- Badge -->
            <g transform="translate(16, 14)">
                <rect width="78" height="18" rx="4" fill="{p['badge_color']}" fill-opacity="0.15" stroke="{p['badge_color']}" stroke-width="1"/>
                <text x="39" y="12.5" fill="{p['badge_text']}" font-size="9" font-weight="700" font-family="{FONTS['mono']}" text-anchor="middle">{p['badgebadge' if 'badgebadge' in p else 'badge']}</text>
            </g>
            
            <!-- Title -->
            <text x="16" y="52" fill="#f8fafc" font-size="16" font-weight="700" font-family="{FONTS['sans']}">{p['name']}</text>
            <text x="16" y="68" fill="#818cf8" font-size="11" font-weight="500" font-family="{FONTS['sans']}">{p['type']}</text>
            
            <!-- Description -->
            <text x="16" y="86" fill="#94a3b8" font-size="11" font-family="{FONTS['sans']}">
                <tspan x="16" dy="0">{p['desc1']}</tspan>
                <tspan x="16" dy="15">{p['desc2']}</tspan>
                <tspan x="16" dy="15">{p['desc3']}</tspan>
            </text>
            
            <!-- Tech Stack Pills -->
            {pills_markup}
        </g>
        """)

    cards_markup = "".join(cards_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="proj-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#080c14" />
            <stop offset="50%" stop-color="#0b101d" />
            <stop offset="100%" stop-color="#070a12" />
        </linearGradient>

        <linearGradient id="proj-border" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1e293b" stop-opacity="0.9"/>
            <stop offset="50%" stop-color="#334155" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#1e293b" stop-opacity="0.9"/>
        </linearGradient>
    </defs>

    <style>
        .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif; }}
        .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, Menlo, monospace; }}
    </style>

    <!-- Background Frame -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#proj-bg)" />
    <rect width="{width}" height="{height}" rx="14" fill="none" stroke="url(#proj-border)" stroke-width="1.2" />

    <!-- Top Header -->
    <g transform="translate(36, 32)">
        <text x="0" y="0" class="font-mono" font-size="11.5" font-weight="700" fill="#2dd4bf" letter-spacing="0.16em">
            FEATURED.SYSTEMS // PRODUCTION ARCHITECTURE
        </text>
        <text x="{width - 72}" y="0" class="font-mono" font-size="10.5" fill="#64748b" text-anchor="end">
            Verified Repositories
        </text>
    </g>

    <!-- Project Cards -->
    {cards_markup}
</svg>"""

    save_svg("projects.svg", svg)

if __name__ == "__main__":
    generate_projects_svg()
