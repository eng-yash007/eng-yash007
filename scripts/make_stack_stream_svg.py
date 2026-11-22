"""
Generates the verified STACK.STREAM card (440x320) with compact, properly aligned technology pills.
Strictly zero clipping, zero horizontal overflow, no unnecessary marquee scrolling.
"""

from utils import THEME, FONTS, escape, save_svg

def generate_stack_stream():
    width = 440
    height = 320

    # 16 verified technologies strictly from Yash's resume and production projects
    rows = [
        # Row 1: Core GenAI & LLMs
        [
            {"name": "GenAI", "color": "#38BDF8"},
            {"name": "LLMs", "color": "#8B5CF6"},
            {"name": "RAG", "color": "#22D3EE"},
            {"name": "LangChain", "color": "#8B5CF6"},
        ],
        # Row 2: Frameworks & Models
        [
            {"name": "FastAPI", "color": "#10B981"},
            {"name": "PyTorch", "color": "#F472B6"},
            {"name": "HF Models", "color": "#FBBF24"},
            {"name": "Llama-3", "color": "#8B5CF6"},
        ],
        # Row 3: Vision & Audio AI
        [
            {"name": "CV Pipeline", "color": "#38BDF8"},
            {"name": "OpenCV", "color": "#10B981"},
            {"name": "YOLOv8", "color": "#FB923C"},
            {"name": "Whisper", "color": "#22D3EE"},
        ],
        # Row 4: Data & Platforms
        [
            {"name": "Python", "color": "#FBBF24"},
            {"name": "Next.js", "color": "#38BDF8"},
            {"name": "pgvector", "color": "#10B981"},
            {"name": "Docker", "color": "#38BDF8"},
        ],
    ]

    pill_w = 93
    pill_h = 32
    gap_x = 9
    start_x = 20.5
    start_y = 66
    gap_y = 12

    pills_markup_list = []
    for r_idx, row in enumerate(rows):
        y = start_y + r_idx * (pill_h + gap_y)
        for c_idx, item in enumerate(row):
            x = start_x + c_idx * (pill_w + gap_x)
            col = item["color"]
            name = item["name"]
            pills_markup_list.append(f"""
            <g transform="translate({x:.1f}, {y})">
                <rect width="{pill_w}" height="{pill_h}" rx="6" fill="#0B1120" stroke="#1E293B" stroke-width="1"/>
                <circle cx="12" cy="16" r="3" fill="{col}"/>
                <text x="{12 + (pill_w - 12)/2}" y="20" fill="#F1F5F9" font-size="11" font-weight="600" font-family="{FONTS['sans']}" text-anchor="middle">
                    {escape(name)}
                </text>
            </g>
            """)

    all_pills = "".join(pills_markup_list)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="stack-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#080D18" />
            <stop offset="50%" stop-color="#0D1424" />
            <stop offset="100%" stop-color="#080D18" />
        </linearGradient>

        <linearGradient id="stack-border" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1E293B" stop-opacity="0.9"/>
            <stop offset="50%" stop-color="#334155" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#1E293B" stop-opacity="0.9"/>
        </linearGradient>
    </defs>

    <!-- Background card -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#stack-bg)" stroke="url(#stack-border)" stroke-width="1.2"/>

    <!-- Corner brackets -->
    <path d="M 18 34 L 18 18 L 34 18" fill="none" stroke="#38BDF8" stroke-width="2" />
    <path d="M 18 {height - 34} L 18 {height - 18} L 34 {height - 18}" fill="none" stroke="#38BDF8" stroke-width="2" />

    <!-- Header bar -->
    <text x="38" y="27" fill="#38BDF8" font-size="12" font-weight="700" font-family="{FONTS['mono']}">STACK.STREAM</text>
    <circle cx="160" cy="22" r="3.5" fill="#10B981" />
    <text x="172" y="26" fill="#94A3B8" font-size="10.5" font-family="{FONTS['mono']}">VERIFIED SKILLS</text>
    
    <!-- Divider -->
    <line x1="18" y1="50" x2="{width - 18}" y2="50" stroke="#1E293B" stroke-width="1" />

    <!-- Grid of Technology Pills (Aligned, Zero Clipping) -->
    {all_pills}

    <!-- Footer caption -->
    <text x="{width / 2}" y="{height - 20}" fill="#64748B" font-size="10.5" font-family="{FONTS['mono']}" text-anchor="middle">
        16 VERIFIED PRODUCTION TECHNOLOGIES
    </text>
</svg>"""

    save_svg("stack_stream.svg", svg)

if __name__ == "__main__":
    generate_stack_stream()
