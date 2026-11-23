"""
Generates the minimal, modern FEATURED.SYSTEMS dashboard card (900x220) for:
1. SILENT GALLERY (Voice AI & Smart Task Workspace)
2. GUARDIAN TRANSIT AI (Computer Vision & Student Safety)
Engineered strictly following the Premium Dark Tech Design System.
"""

from utils import THEME, FONTS, escape, save_svg

def generate_projects_svg():
    width = 900
    height = 220
    card_w = 404
    card_h = 144
    gap = 20
    start_x = 36
    start_y = 52

    projects = [
        {
            "name": "Silent Gallery",
            "type": "Voice AI & Smart Task Workspace",
            "badge": "Live Demo",
            "accent": "#A78BFA",
            "desc1": "Voice productivity hub powered by Whisper & Llama-3 for",
            "desc2": "hands-free task execution and automated calendar scheduling.",
            "stack": ["Next.js", "Llama-3", "Whisper", "Supabase", "FastAPI"],
            "url": "https://silent-galleryyy.vercel.app",
            "repo": "https://github.com/eng-yash007/silent_gallery"
        },
        {
            "name": "Guardian Transit AI",
            "type": "Computer Vision & Student Safety",
            "badge": "Live Demo",
            "accent": "#38BDF8",
            "desc1": "Real-time edge CV pipeline with YOLOv8 & ArcFace embeddings,",
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
            tw = len(tech) * 6.5 + 16
            pills_svg.append(f"""
            <rect x="{p_x:.1f}" y="{start_y + 104}" width="{tw:.1f}" height="20" rx="4" fill="#0D1424" stroke="#1E293B" stroke-width="1"/>
            <text x="{p_x + tw/2:.1f}" y="{start_y + 118}" fill="#94A3B8" font-size="10" font-family="{FONTS['mono']}" text-anchor="middle">{escape(tech)}</text>
            """)
            p_x += tw + 8
        pills_markup = "".join(pills_svg)

        cards_svg.append(f"""
        <!-- Card {i+1}: {p['name']} -->
        <g class="project-card">
            <!-- Card Outer Surface -->
            <rect x="{cx}" y="{start_y}" width="{card_w}" height="{card_h}" rx="10" fill="url(#card-inner-bg)" stroke="#1E293B" stroke-width="1.1"/>
            
            <!-- Title & Status Badge -->
            <g transform="translate({cx + 20}, {start_y + 24})">
                <text x="0" y="0" fill="#F8FAFC" font-size="16" font-weight="700" font-family="{FONTS['sans']}">{escape(p['name'])}</text>
                
                <!-- Minimal Status Badge -->
                <g transform="translate({card_w - 40}, 0)">
                    <rect x="-80" y="-12" width="80" height="18" rx="4" fill="#10B981" fill-opacity="0.12" stroke="#10B981" stroke-width="0.8"/>
                    <circle cx="-70" cy="-3" r="2.5" fill="#34D399" />
                    <text x="-36" y="0.5" fill="#34D399" font-size="9.5" font-weight="600" font-family="{FONTS['mono']}" text-anchor="middle">{escape(p['badge'])}</text>
                </g>
            </g>
            
            <!-- Category / Subtitle -->
            <text x="{cx + 20}" y="{start_y + 44}" fill="{p['accent']}" font-size="11.5" font-weight="600" font-family="{FONTS['sans']}">{escape(p['type'])}</text>
            
            <!-- Description -->
            <text x="{cx + 20}" y="{start_y + 65}" fill="#94A3B8" font-size="11.5" font-family="{FONTS['sans']}">
                <tspan x="{cx + 20}" dy="0">{escape(p['desc1'])}</tspan>
                <tspan x="{cx + 20}" dy="16">{escape(p['desc2'])}</tspan>
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

        <linearGradient id="card-inner-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0B1120" />
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
    </style>

    <!-- Outer Container -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#proj-bg)" stroke="url(#proj-border)" stroke-width="1.2"/>
    
    <!-- Header -->
    <g transform="translate(36, 31)">
        <text x="0" y="0" fill="#38BDF8" font-size="11.5" font-weight="700" font-family="{FONTS['mono']}" letter-spacing="0.16em">FEATURED.SYSTEMS // PRODUCTION DEPLOYMENTS</text>
        <text x="{width - 72}" y="0" fill="#64748B" font-size="10" font-family="{FONTS['mono']}" text-anchor="end"><tspan fill="#34D399">● </tspan>2 FLAGSHIPS ACTIVE</text>
    </g>

    {all_cards}
</svg>"""

    save_svg("projects.svg", svg)

if __name__ == "__main__":
    generate_projects_svg()
