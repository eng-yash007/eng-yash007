"""
Generates the balanced, static, zero-overflow STACK.STREAM SVG (440x320).
Strictly matches VISUAL.MAP dimensions, header alignment, border thickness, and corner styling.
Completely removes marquee movement; organizes 14 core verified technologies into 4 clean,
mathematically centered, perfectly spaced horizontal rows with zero clipping.
"""

from utils import FONTS, escape, save_svg

def generate_stack_stream():
    width = 440
    height = 320

    # 14 core verified technologies grouped into 4 balanced horizontal rows
    rows_data = [
        # Row 1: 4 core languages & full-stack web
        [
            {"name": "Python", "w": 74, "border": "#FBBF24", "dot": "#FBBF24"},
            {"name": "FastAPI", "w": 78, "border": "#22D3EE", "dot": "#22D3EE"},
            {"name": "Next.js", "w": 78, "border": "#38BDF8", "dot": "#38BDF8"},
            {"name": "C++", "w": 62, "border": "#818CF8", "dot": "#818CF8"},
        ],
        # Row 2: 3 primary AI/ML frameworks
        [
            {"name": "LangChain", "w": 100, "border": "#8B5CF6", "dot": "#8B5CF6"},
            {"name": "Hugging Face", "w": 116, "border": "#FBBF24", "dot": "#FBBF24"},
            {"name": "PyTorch", "w": 86, "border": "#FB923C", "dot": "#FB923C"},
        ],
        # Row 3: 4 production backend & vector infrastructure
        [
            {"name": "Docker", "w": 76, "border": "#38BDF8", "dot": "#38BDF8"},
            {"name": "PostgreSQL", "w": 102, "border": "#818CF8", "dot": "#818CF8"},
            {"name": "FAISS", "w": 72, "border": "#22D3EE", "dot": "#22D3EE"},
            {"name": "SQL", "w": 60, "border": "#34D399", "dot": "#34D399"},
        ],
        # Row 4: 3 specialized intelligence & toolchain
        [
            {"name": "Whisper", "w": 84, "border": "#8B5CF6", "dot": "#8B5CF6"},
            {"name": "Computer Vision", "w": 136, "border": "#38BDF8", "dot": "#38BDF8"},
            {"name": "Git", "w": 60, "border": "#F87171", "dot": "#F87171"},
        ]
    ]

    row_y_starts = [68, 118, 168, 218]
    pill_h = 32

    rows_markup = []

    for r_idx, items in enumerate(rows_data):
        y_pos = row_y_starts[r_idx]
        gap = 10
        total_w = sum(it["w"] for it in items) + gap * (len(items) - 1)
        start_x = (width - total_w) / 2.0  # Mathematically centered within 440px width

        current_x = start_x
        for it in items:
            pw = it["w"]
            dot_color = it["dot"]
            border_color = it["border"]
            name = escape(it["name"])

            rows_markup.append(f"""
        <!-- Pill: {name} -->
        <g transform="translate({current_x:.1f}, {y_pos})">
            <rect width="{pw}" height="{pill_h}" rx="8" fill="#0D1424" stroke="{border_color}" stroke-opacity="0.65" stroke-width="1.1"/>
            <circle cx="14" cy="16" r="3" fill="{dot_color}"/>
            <text x="{14 + 10}" y="20" fill="#F1F5F9" font-size="11.5" font-weight="600" font-family="{FONTS['sans']}">
                {name}
            </text>
        </g>
            """)
            current_x += pw + gap

    all_pills_svg = "".join(rows_markup)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="stack-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#080D18" />
            <stop offset="50%" stop-color="#0D1424" />
            <stop offset="100%" stop-color="#080D18" />
        </linearGradient>
    </defs>

    <style>
        .font-sans {{ font-family: {FONTS['sans']}; }}
        .font-mono {{ font-family: {FONTS['mono']}; }}
    </style>

    <!-- Outer Frame (Strictly identical to VISUAL.MAP) -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#stack-bg)" stroke="#1E293B" stroke-width="1" />

    <!-- Corner Brackets -->
    <path d="M 18 34 L 18 18 L 34 18" fill="none" stroke="#38BDF8" stroke-width="2" />
    <path d="M 18 {height - 34} L 18 {height - 18} L 34 {height - 18}" fill="none" stroke="#38BDF8" stroke-width="2" />

    <!-- Header Bar -->
    <text x="38" y="25" fill="#38BDF8" font-size="12" font-weight="700" class="font-mono">STACK.STREAM</text>
    <circle cx="152" cy="21" r="3" fill="#34D399" />
    <text x="164" y="25" fill="#64748B" font-size="10.5" class="font-mono">VERIFIED MATRIX</text>
    
    <!-- Divider -->
    <line x1="18" y1="48" x2="{width - 18}" y2="48" stroke="#1E293B" stroke-width="1" />

    <!-- 4 Balanced Horizontal Rows of Pills -->
    <g class="stack-grid">
{all_pills_svg}
    </g>

    <!-- Bottom Caption -->
    <text x="{width / 2}" y="{height - 20}" fill="#64748B" font-size="11" class="font-mono" text-anchor="middle">
        production.verified · 14 core skills
    </text>
</svg>"""

    save_svg("stack_stream.svg", svg)

if __name__ == "__main__":
    generate_stack_stream()
