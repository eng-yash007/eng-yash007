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
    # Place items once
    x = 0
    elements = []
    for item in items:
        markup, w = build_pill(x, item)
        elements.append(markup)
        x += w + 12
    total_single_width = x
    
    # Place duplicate items immediately after for seamless loop
    for item in items:
        markup, w = build_pill(x, item)
        elements.append(markup)
        x += w + 12
        
    return "".join(elements), total_single_width

def generate_stack_stream():
    width = 440
    height = 360

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
        {"name": "WebSockets", "color": "#f472b6", "dot": "#db2777"},
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

        <linearGradient id="neon-border" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.85" />
            <stop offset="50%" stop-color="#818cf8" stop-opacity="0.5" />
            <stop offset="100%" stop-color="#ec4899" stop-opacity="0.85" />
        </linearGradient>

        <radialGradient id="stack-ambient" cx="80%" cy="30%" r="60%">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.14" />
            <stop offset="60%" stop-color="#818cf8" stop-opacity="0.06" />
            <stop offset="100%" stop-color="#000000" stop-opacity="0" />
        </radialGradient>

        <!-- Clip Path to keep streaming pills strictly within container borders -->
        <clipPath id="inner-stream-clip">
            <rect x="16" y="60" width="{width - 32}" height="{height - 76}" rx="10" />
        </clipPath>
    </defs>

    <style>
        .font-sans {{ font-family: {FONTS['sans']}; }}
        .font-mono {{ font-family: {FONTS['mono']}; }}

        /* Row 1 Stream Animation (Leftwards) */
        @keyframes streamRow1 {{
            0% {{
                transform: translateX(0px);
            }}
            100% {{
                transform: translateX(-{r1_width}px);
            }}
        }}

        /* Row 2 Stream Animation (Rightwards) */
        @keyframes streamRow2 {{
            0% {{
                transform: translateX(-{r2_width}px);
            }}
            100% {{
                transform: translateX(0px);
            }}
        }}

        /* Row 3 Stream Animation (Leftwards, slightly different tempo) */
        @keyframes streamRow3 {{
            0% {{
                transform: translateX(0px);
            }}
            100% {{
                transform: translateX(-{r3_width}px);
            }}
        }}

        .row1 {{
            animation: streamRow1 16s linear infinite;
        }}
        .row2 {{
            animation: streamRow2 18s linear infinite;
        }}
        .row3 {{
            animation: streamRow3 15s linear infinite;
        }}

        /* Live Indicator Blink */
        @keyframes streamDotPulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}
        .stream-live {{
            animation: streamDotPulse 1.4s infinite ease-in-out;
        }}
    </style>

    <!-- Card Base -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#stack-bg)" />
    <rect width="{width}" height="{height}" rx="14" fill="url(#stack-ambient)" />
    
    <!-- Outer Neon Glow Border -->
    <rect x="12" y="12" width="{width - 24}" height="{height - 24}" rx="12" fill="none" stroke="url(#neon-border)" stroke-width="1.4" />

    <!-- Top Label Bar -->
    <g transform="translate(26, 38)">
        <text x="0" y="0" class="font-mono" font-size="12.5" font-weight="700" fill="#38bdf8" letter-spacing="0.18em">
            STACK.STREAM
        </text>

        <!-- Live Streaming Pill Tag -->
        <g transform="translate(136, -14)">
            <rect width="96" height="20" rx="5" fill="#1e293b" fill-opacity="0.8" stroke="#334155" stroke-width="1"/>
            <circle cx="12" cy="10" r="3.5" fill="#2dd4bf" class="stream-live"/>
            <text x="22" y="14" fill="#94a3b8" font-size="11" font-weight="600" class="font-mono">
                LIVE FLOW
            </text>
        </g>
    </g>

    <!-- Clipped Stream Rows -->
    <g clip-path="url(#inner-stream-clip)">
        <!-- Row 1 -->
        <g transform="translate(0, 80)">
            <g class="row1">
                {row1_markup}
            </g>
        </g>

        <!-- Row 2 -->
        <g transform="translate(0, 155)">
            <g class="row2">
                {row2_markup}
            </g>
        </g>

        <!-- Row 3 -->
        <g transform="translate(0, 230)">
            <g class="row3">
                {row3_markup}
            </g>
        </g>
    </g>
</svg>"""

    save_svg("stack_stream.svg", svg)

if __name__ == "__main__":
    generate_stack_stream()
