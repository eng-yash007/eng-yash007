from utils import THEME, FONTS, escape, save_svg

def build_pill(x, item):
    name = item["name"]
    color = item["color"]
    dot = item["dot"]
    pill_w = max(len(name) * 8.5 + 32, 74)
    
    markup = f"""
    <g transform="translate({x}, 0)">
        <rect width="{pill_w}" height="36" rx="18" fill="#0D1424" stroke="{color}" stroke-width="1.2" />
        <circle cx="15" cy="18" r="3.5" fill="{dot}" />
        <text x="26" y="22" fill="#F1F5F9" font-size="12" font-weight="600" class="font-sans">
            {escape(name)}
        </text>
    </g>
    """
    return markup, pill_w

def build_row_elements(items):
    x = 0
    elements = []
    for item in items:
        markup, w = build_pill(x, item)
        elements.append(markup)
        x += w + 12
    total_single_width = x
    
    for item in items:
        markup, w = build_pill(x, item)
        elements.append(markup)
        x += w + 12
        
    return "".join(elements), total_single_width

def generate_stack_stream():
    # Symmetrically matched with VISUAL.MAP: 440x320
    width = 440
    height = 320

    row1_items = [
        {"name": "Next.js", "color": "#38BDF8", "dot": "#0284C7"},
        {"name": "FastAPI", "color": "#22D3EE", "dot": "#0891B2"},
        {"name": "Python", "color": "#FBBF24", "dot": "#D97706"},
        {"name": "C++", "color": "#60A5FA", "dot": "#2563EB"},
        {"name": "TypeScript", "color": "#38BDF8", "dot": "#0284C7"},
        {"name": "SQL", "color": "#22D3EE", "dot": "#0891B2"}
    ]

    row2_items = [
        {"name": "PyTorch", "color": "#FB923C", "dot": "#EA580C"},
        {"name": "LangChain", "color": "#8B5CF6", "dot": "#7C3AED"},
        {"name": "OpenCV", "color": "#34D399", "dot": "#059669"},
        {"name": "Docker", "color": "#38BDF8", "dot": "#0284C7"},
        {"name": "Llama-3", "color": "#8B5CF6", "dot": "#6D28D9"},
        {"name": "Hugging Face", "color": "#FBBF24", "dot": "#D97706"}
    ]

    row3_items = [
        {"name": "PostgreSQL", "color": "#818CF8", "dot": "#4F46E5"},
        {"name": "pgvector", "color": "#22D3EE", "dot": "#0891B2"},
        {"name": "Whisper", "color": "#8B5CF6", "dot": "#7C3AED"},
        {"name": "Git", "color": "#F87171", "dot": "#DC2626"},
        {"name": "Linux", "color": "#FBBF24", "dot": "#D97706"},
        {"name": "Vercel", "color": "#CBD5E1", "dot": "#94A3B8"}
    ]

    row1_markup, r1_width = build_row_elements(row1_items)
    row2_markup, r2_width = build_row_elements(row2_items)
    row3_markup, r3_width = build_row_elements(row3_items)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="stack-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#080D18" />
            <stop offset="50%" stop-color="#0D1424" />
            <stop offset="100%" stop-color="#080D18" />
        </linearGradient>

        <clipPath id="inner-stream-clip">
            <rect x="16" y="52" width="{width - 32}" height="{height - 86}" rx="8" />
        </clipPath>

        <linearGradient id="left-fade" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#080D18" stop-opacity="0.95" />
            <stop offset="100%" stop-color="#080D18" stop-opacity="0" />
        </linearGradient>
        <linearGradient id="right-fade" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#080D18" stop-opacity="0" />
            <stop offset="100%" stop-color="#080D18" stop-opacity="0.95" />
        </linearGradient>
    </defs>

    <style>
        .font-sans {{ font-family: {FONTS['sans']}; }}
        .font-mono {{ font-family: {FONTS['mono']}; }}

        @keyframes streamRow1 {{
            0% {{ transform: translateX(0px); }}
            100% {{ transform: translateX(-{r1_width}px); }}
        }}
        @keyframes streamRow2 {{
            0% {{ transform: translateX(-{r2_width}px); }}
            100% {{ transform: translateX(0px); }}
        }}
        @keyframes streamRow3 {{
            0% {{ transform: translateX(0px); }}
            100% {{ transform: translateX(-{r3_width}px); }}
        }}

        .row-stream-1 {{ animation: streamRow1 28s linear infinite; }}
        .row-stream-2 {{ animation: streamRow2 32s linear infinite; }}
        .row-stream-3 {{ animation: streamRow3 30s linear infinite; }}

        .stream-viewport:hover .row-stream-1,
        .stream-viewport:hover .row-stream-2,
        .stream-viewport:hover .row-stream-3 {{
            animation-play-state: paused;
        }}
    </style>

    <!-- Outer Frame -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#stack-bg)" stroke="#1E293B" stroke-width="1" />

    <!-- Corner brackets -->
    <path d="M 18 34 L 18 18 L 34 18" fill="none" stroke="#38BDF8" stroke-width="2" />
    <path d="M 18 {height - 34} L 18 {height - 18} L 34 {height - 18}" fill="none" stroke="#38BDF8" stroke-width="2" />

    <!-- Header bar -->
    <text x="38" y="25" fill="#38BDF8" font-size="12" font-weight="700" class="font-mono">STACK.STREAM</text>
    <circle cx="160" cy="21" r="3.5" fill="#22C55E" />
    <text x="170" y="25" fill="#64748B" font-size="10.5" class="font-mono">LIVE MATRIX</text>
    
    <!-- Divider -->
    <line x1="18" y1="48" x2="{width - 18}" y2="48" stroke="#1E293B" stroke-width="1" />

    <!-- Streaming viewport -->
    <g class="stream-viewport" clip-path="url(#inner-stream-clip)">
        <!-- Row 1 -->
        <g transform="translate(0, 66)">
            <g class="row-stream-1">
                {row1_markup}
            </g>
        </g>

        <!-- Row 2 -->
        <g transform="translate(0, 138)">
            <g class="row-stream-2">
                {row2_markup}
            </g>
        </g>

        <!-- Row 3 -->
        <g transform="translate(0, 210)">
            <g class="row-stream-3">
                {row3_markup}
            </g>
        </g>
    </g>

    <!-- Edge vignettes -->
    <rect x="16" y="52" width="28" height="{height - 86}" fill="url(#left-fade)" pointer-events="none" />
    <rect x="{width - 44}" y="52" width="28" height="{height - 86}" fill="url(#right-fade)" pointer-events="none" />

    <!-- Footer caption -->
    <text x="{width / 2}" y="{height - 20}" fill="#64748B" font-size="10.5" class="font-mono" text-anchor="middle">
        CONTINUOUS PIPELINE • 18 TECHNOLOGIES
    </text>
</svg>"""

    save_svg("stack_stream.svg", svg)

if __name__ == "__main__":
    generate_stack_stream()
