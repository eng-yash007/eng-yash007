import json
from utils import THEME, FONTS, escape, save_svg

def generate_hero():
    with open("data/profile.json", "r", encoding="utf-8") as f:
        profile = json.load(f)

    name = profile.get("name", "Yash Gupta")
    first_name = name.split()[0] if name else "Yash"
    batch = profile.get("batch", "Batch 2027")
    status_pill = f"Open to opportunities  ·  {batch}"
    
    typing_text = "I build safer transport systems & intelligent AI agents"
    sub_text_1 = "Final-year Computer Science (Data Science) student turning computer"
    sub_text_2 = "vision and GenAI into systems that actually run in the real world."

    width = 900
    height = 250

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <!-- Background Gradients -->
        <linearGradient id="hero-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#07090e" />
            <stop offset="50%" stop-color="#0b101b" />
            <stop offset="100%" stop-color="#080c14" />
        </linearGradient>

        <!-- Ambient Glow -->
        <radialGradient id="ambient-glow" cx="80%" cy="10%" r="60%">
            <stop offset="0%" stop-color="#6366f1" stop-opacity="0.18" />
            <stop offset="50%" stop-color="#2dd4bf" stop-opacity="0.08" />
            <stop offset="100%" stop-color="#000000" stop-opacity="0" />
        </radialGradient>

        <!-- Yash Gradient -->
        <linearGradient id="name-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#818cf8" />
            <stop offset="50%" stop-color="#a78bfa" />
            <stop offset="100%" stop-color="#2dd4bf" />
        </linearGradient>

        <linearGradient id="pill-border" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#334155" />
            <stop offset="100%" stop-color="#1e293b" />
        </linearGradient>

        <!-- Card Glow Border -->
        <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#334155" stop-opacity="0.7"/>
            <stop offset="50%" stop-color="#1e293b" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#0f172a" stop-opacity="0.8"/>
        </linearGradient>
    </defs>

    <style>
        .font-sans {{ font-family: {FONTS['sans']}; }}
        .font-mono {{ font-family: {FONTS['mono']}; }}

        /* Status Beacon Pulse */
        @keyframes pulseDot {{
            0% {{ r: 4px; opacity: 1; }}
            50% {{ r: 6.5px; opacity: 0.4; }}
            100% {{ r: 4px; opacity: 1; }}
        }}
        .beacon {{
            animation: pulseDot 2s infinite ease-in-out;
            transform-origin: 52px 42px;
        }}

        /* Cursor Blink */
        @keyframes blink {{
            0%, 49% {{ opacity: 1; }}
            50%, 100% {{ opacity: 0; }}
        }}
        .cursor {{
            animation: blink 0.9s infinite;
        }}

        /* Typewriter Clip */
        @keyframes typeIn {{
            from {{ width: 0; }}
            to {{ width: 100%; }}
        }}
        .typing-box {{
            overflow: hidden;
            white-space: nowrap;
            display: inline-block;
        }}
    </style>

    <!-- Card Base -->
    <rect width="{width}" height="{height}" rx="16" fill="url(#hero-bg)" />
    <rect width="{width}" height="{height}" rx="16" fill="url(#ambient-glow)" />
    <rect width="{width}" height="{height}" rx="16" fill="none" stroke="url(#border-grad)" stroke-width="1.2" />

    <!-- Status Pill: Open to opportunities -->
    <g transform="translate(36, 28)">
        <rect width="250" height="28" rx="14" fill="#0f172a" fill-opacity="0.9" stroke="#334155" stroke-width="1"/>
        <!-- Green indicator -->
        <circle cx="16" cy="14" r="5" fill="#10b981" />
        <circle cx="16" cy="14" r="7" fill="#10b981" opacity="0.3" class="beacon"/>
        <text x="32" y="18.5" fill="#94a3b8" font-size="12" font-weight="500" class="font-sans">
            {escape(status_pill)}
        </text>
    </g>

    <!-- Big Heading: Hi, I'm Yash. -->
    <text x="36" y="112" class="font-sans" font-size="44" font-weight="800" fill="#f8fafc" letter-spacing="-0.03em">
        Hi, I'm <tspan fill="url(#name-grad)">{escape(first_name)}.</tspan>
    </text>

    <!-- Animated Typewriter Subheading -->
    <g transform="translate(36, 150)">
        <text x="0" y="0" class="font-sans" font-size="20" font-weight="500" fill="#94a3b8">
            <tspan fill="#f1f5f9" font-weight="600">{escape(typing_text)}</tspan>
        </text>
        <!-- Typewriter vertical bar cursor -->
        <line x1="530" y1="-16" x2="530" y2="4" stroke="#818cf8" stroke-width="2.5" stroke-linecap="round" class="cursor"/>
    </g>

    <!-- Description Paragraph -->
    <text x="36" y="196" class="font-sans" font-size="14.5" fill="#94a3b8" letter-spacing="-0.01em">
        {escape(sub_text_1)}
    </text>
    <text x="36" y="220" class="font-sans" font-size="14.5" fill="#94a3b8" letter-spacing="-0.01em">
        {escape(sub_text_2)}
    </text>
</svg>"""

    save_svg("hero.svg", svg)

if __name__ == "__main__":
    generate_hero()

