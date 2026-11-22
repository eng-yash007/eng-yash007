from utils import THEME, FONTS, escape, save_svg

def build_pill(x, item):
    name = item["name"]
    color = item["color"]
    dot = item["dot"]
    pill_w = max(len(name) * 8.5 + 34, 76)
    
    markup = f"""
    <g transform="translate({x}, 0)">
        <rect width="{pill_w}" height="38" rx="19" fill="#0f172a" fill-opacity="0.9" stroke="{color}" stroke-width="1.3" />
        <circle cx="16" cy="19" r="4" fill="{dot}" />
        <text x="28" y="23.5" fill="#f1f5f9" font-size="12.5" font-weight="600" class="font-sans">
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
    # Symmetrically matched with VISUAL.MAP: 440x340
    width = 440
    height = 340

    row1_items = [
        {"name": "Next.js", "color": "#38bdf8", "dot": "#0284c7"},
        {"name": "FastAPI", "color": "#2dd4bf", "dot": "#0d9488"},
        {"name": "Python", "color": "#fbbf24", "dot": "#d97706"},
        {"name": "C++", "color": "#60a5fa", "dot": "#2563eb"},
        {"name": "TypeScript", "color": "#38bdf8", "dot": "#0284c7"},
        {"name": "SQL", "color": "#2dd4bf", "dot": "#0d9488"}
    ]

    row2_items = [
        {"name": "PyTorch", "color": "#fb923c", "dot": "#ea580c"},
        {"name": "LangChain", "color": "#c084fc", "dot": "#9333ea"},
        {"name": "OpenCV", "color": "#4ade80", "dot": "#16a34a"},
        {"name": "Docker", "color": "#38bdf8", "dot": "#0284c7"},
        {"name": "Llama-3", "color": "#a855f7", "dot": "#7e22ce"},
        {"name": "Hugging Face", "color": "#fbbf24", "dot": "#d97706"}
    ]

    row3_items = [
        {"name": "PostgreSQL", "color": "#818cf8", "dot": "#4f46e5"},
        {"name": "pgvector", "color": "#34d399", "dot": "#059669"},
        {"name": "Whisper", "color": "#c084fc", "dot": "#9333ea"},
        {"name": "Git", "color": "#f87171", "dot": "#dc2626"},
        {"name": "Linux", "color": "#fbbf24", "dot": "#d97706"},
        {"name": "Vercel", "color": "#e2e8f0", "dot": "#94a3b8"}
    ]

    row1_markup, r1_width = build_row_elements(row1_items)
    row2_markup, r2_width = build_row_elements(row2_items)
    row3_markup, r3_width = build_row_elements(row3_items)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="stack-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#060911" />
            <stop offset="50%" stop-color="#0b101d" />
            <stop offset="100%" stop-color="#060810" />
        </linearGradient>

        <radialGradient id="stack-ambient" cx="80%" cy="30%" r="60%">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.14" />
            <stop offset="60%" stop-color="#818cf8" stop-opacity="0.06" />
            <stop offset="100%" stop-color="#000000" stop-opacity="0" />
        </radialGradient>

        <clipPath id="inner-stream-clip">
            <rect x="16" y="56" width="{width - 32}" height="{height - 96}" rx="10" />
        </clipPath>
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

        .row-stream-1 {{
            animation: streamRow1 30s linear infinite;
        }}
        .row-stream-2 {{
            animation: streamRow2 34s linear infinite;
        }}
        .row-stream-3 {{
            animation: streamRow3 32s linear infinite;
        }}

        .stream-viewport:hover .row-stream-1,
        .stream-viewport:hover .row-stream-2,
        .stream-viewport:hover .row-stream-3 {{
            animation-play-state: paused;
        }}
    </style>

    <!-- Background card -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#stack-bg)" />
    <rect width="{width}" height="{height}" rx="14" fill="url(#stack-ambient)" />
    <rect width="{width}" height="{height}" rx="14" fill="none" stroke="#18202f" stroke-width="1" />

    <!-- Corner brackets -->
    <path d="M 18 36 L 18 18 L 36 18" fill="none" stroke="#38bdf8" stroke-width="2" />
    <path d="M 18 {height - 36} L 18 {height - 18} L 36 {height - 18}" fill="none" stroke="#38bdf8" stroke-width="2" />

    <!-- Header bar -->
    <text x="40" y="27" fill="#38bdf8" font-size="13" font-weight="700" class="font-mono">STACK.STREAM</text>
    <circle cx="165" cy="22" r="3.5" fill="#22c55e" />
    <text x="176" y="26" fill="#64748b" font-size="11" class="font-mono">LIVE MATRIX</text>
    
    <!-- Divider -->
    <line x1="18" y1="52" x2="{width - 18}" y2="52" stroke="#18202f" stroke-width="1" />

    <!-- Streaming viewport -->
    <g class="stream-viewport" clip-path="url(#inner-stream-clip)">
        <!-- Row 1 -->
        <g transform="translate(0, 72)">
            <g class="row-stream-1">
                {row1_markup}
            </g>
        </g>

        <!-- Row 2 -->
        <g transform="translate(0, 150)">
            <g class="row-stream-2">
                {row2_markup}
            </g>
        </g>

        <!-- Row 3 -->
        <g transform="translate(0, 228)">
            <g class="row-stream-3">
                {row3_markup}
            </g>
        </g>
    </g>

    <!-- Edge vignettes -->
    <rect x="16" y="56" width="30" height="{height - 96}" fill="url(#left-fade)" pointer-events="none" />
    <rect x="{width - 46}" y="56" width="30" height="{height - 96}" fill="url(#right-fade)" pointer-events="none" />

    <defs>
        <linearGradient id="left-fade" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#080c16" stop-opacity="0.95" />
            <stop offset="100%" stop-color="#080c16" stop-opacity="0" />
        </linearGradient>
        <linearGradient id="right-fade" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#080c16" stop-opacity="0" />
            <stop offset="100%" stop-color="#080c16" stop-opacity="0.95" />
        </linearGradient>
    </defs>

    <!-- Footer caption -->
    <text x="{width / 2}" y="{height - 22}" fill="#64748b" font-size="11" class="font-mono" text-anchor="middle">
        CONTINUOUS PIPELINE • 18 TECHNOLOGIES
    </text>
</svg>"""

    save_svg("stack_stream.svg", svg)

if __name__ == "__main__":
    generate_stack_stream()
