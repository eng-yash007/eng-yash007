import random
import math
from utils import THEME, FONTS, save_svg

def generate_visual_map():
    width = 440
    height = 360

    # Seed for deterministic beautiful particle field
    rng = random.Random(42)

    # Generate stipple points for 'Y' and 'G'
    points = []
    
    # Letter 'Y' (left side centered around x=130)
    # Left branch (x: 85 -> 130, y: 125 -> 195)
    for t in range(45):
        prog = t / 44.0
        x = 85 + (130 - 85) * prog + rng.gauss(0, 3.5)
        y = 125 + (195 - 125) * prog + rng.gauss(0, 3.5)
        points.append((x, y))
    
    # Right branch (x: 175 -> 130, y: 125 -> 195)
    for t in range(45):
        prog = t / 44.0
        x = 175 + (130 - 175) * prog + rng.gauss(0, 3.5)
        y = 125 + (195 - 125) * prog + rng.gauss(0, 3.5)
        points.append((x, y))
        
    # Stem (x: 130, y: 195 -> 265)
    for t in range(45):
        prog = t / 44.0
        x = 130 + rng.gauss(0, 3.5)
        y = 195 + (265 - 195) * prog + rng.gauss(0, 3.5)
        points.append((x, y))

    # Letter 'G' (right side centered around x=295, y=195, r=65)
    for t in range(85):
        prog = t / 84.0
        angle = 0.8 + prog * 4.6  # radians
        r = 65 + rng.gauss(0, 4.0)
        x = 295 + r * math.cos(angle)
        y = 195 + r * math.sin(angle)
        points.append((x, y))
        
    # Crossbar of 'G' (from x=295, y=195 to x=345, y=195)
    for t in range(25):
        prog = t / 24.0
        x = 295 + (345 - 295) * prog + rng.gauss(0, 3)
        y = 195 + rng.gauss(0, 3)
        points.append((x, y))

    # Downward spur of 'G' (from x=345, y=195 to x=345, y=235)
    for t in range(20):
        prog = t / 19.0
        x = 345 + rng.gauss(0, 3)
        y = 195 + (235 - 195) * prog + rng.gauss(0, 3)
        points.append((x, y))

    particle_colors = [
        "#f472b6", "#ec4899", "#d946ef", "#c084fc", "#a855f7", "#818cf8", "#38bdf8"
    ]

    particles_svg = []
    # 5 different animation classes for rich shimmering dynamics
    for i, (px, py) in enumerate(points):
        color = rng.choice(particle_colors)
        radius = rng.uniform(2.2, 4.0)
        opacity = rng.uniform(0.7, 1.0)
        anim_class = f"glow-p{i % 6}"
        particles_svg.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{radius:.1f}" fill="{color}" class="{anim_class}" />'
        )

    dots_str = "\n        ".join(particles_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="vmap-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#05070d" />
            <stop offset="50%" stop-color="#090d18" />
            <stop offset="100%" stop-color="#04060b" />
        </linearGradient>

        <radialGradient id="vmap-glow" cx="50%" cy="50%" r="55%">
            <stop offset="0%" stop-color="#a855f7" stop-opacity="0.25" />
            <stop offset="45%" stop-color="#38bdf8" stop-opacity="0.12" />
            <stop offset="100%" stop-color="#000000" stop-opacity="0" />
        </radialGradient>

        <!-- Laser Scanner Gradient -->
        <linearGradient id="laser-beam" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0" />
            <stop offset="85%" stop-color="#38bdf8" stop-opacity="0.3" />
            <stop offset="100%" stop-color="#22d3ee" stop-opacity="0.85" />
        </linearGradient>

        <linearGradient id="laser-line" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.1" />
            <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.9" />
            <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.1" />
        </linearGradient>
    </defs>

    <style>
        .font-sans {{ font-family: {FONTS['sans']}; }}
        .font-mono {{ font-family: {FONTS['mono']}; }}

        /* Scanning Laser Bar Animation */
        @keyframes scanMotion {{
            0% {{
                transform: translateY(0px);
                opacity: 0;
            }}
            15% {{
                opacity: 0.9;
            }}
            85% {{
                opacity: 0.9;
            }}
            100% {{
                transform: translateY(240px);
                opacity: 0;
            }}
        }}

        .scanner {{
            animation: scanMotion 3.8s ease-in-out infinite;
        }}

        /* Particle Twinkling & Breathing animations */
        @keyframes glow0 {{ 0%, 100% {{ opacity: 0.35; transform: scale(0.9); }} 50% {{ opacity: 1; transform: scale(1.15); }} }}
        @keyframes glow1 {{ 0%, 100% {{ opacity: 0.95; transform: scale(1.1); }} 50% {{ opacity: 0.4; transform: scale(0.9); }} }}
        @keyframes glow2 {{ 0%, 100% {{ opacity: 0.5; }} 50% {{ opacity: 1; }} }}
        @keyframes glow3 {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
        @keyframes glow4 {{ 0%, 100% {{ opacity: 0.4; transform: scale(0.95); }} 50% {{ opacity: 0.95; transform: scale(1.1); }} }}
        @keyframes glow5 {{ 0%, 100% {{ opacity: 0.85; }} 50% {{ opacity: 0.45; }} }}

        .glow-p0 {{ animation: glow0 2.2s infinite ease-in-out; transform-origin: 130px 195px; }}
        .glow-p1 {{ animation: glow1 2.8s infinite ease-in-out 0.4s; transform-origin: 295px 195px; }}
        .glow-p2 {{ animation: glow2 3.1s infinite ease-in-out 0.8s; }}
        .glow-p3 {{ animation: glow3 2.5s infinite ease-in-out 1.2s; }}
        .glow-p4 {{ animation: glow4 3.4s infinite ease-in-out 0.3s; transform-origin: 130px 195px; }}
        .glow-p5 {{ animation: glow5 2.7s infinite ease-in-out 0.7s; }}

        /* Live status dot blinking */
        @keyframes livePulse {{
            0%, 100% {{ opacity: 1; r: 3.5px; }}
            50% {{ opacity: 0.3; r: 5px; }}
        }}
        .live-dot {{
            animation: livePulse 1.6s infinite ease-in-out;
        }}
    </style>

    <!-- Card Background -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#vmap-bg)" />
    <rect width="{width}" height="{height}" rx="14" fill="url(#vmap-glow)" />
    <rect width="{width}" height="{height}" rx="14" fill="none" stroke="#1e293b" stroke-width="1.2" />

    <!-- Corner technical brackets & top bar (from screenshot) -->
    <path d="M 18 36 L 18 18 L 36 18" stroke="#38bdf8" stroke-width="2" fill="none" />
    <line x1="18" y1="52" x2="{width - 18}" y2="52" stroke="#1e293b" stroke-width="1.2" />
    <path d="M 18 {height - 36} L 18 {height - 18} L 36 {height - 18}" stroke="#38bdf8" stroke-width="2" fill="none" />

    <!-- Header label: VISUAL.MAP -->
    <text x="36" y="38" class="font-mono" font-size="13" font-weight="700" fill="#38bdf8" letter-spacing="0.2em">
        VISUAL.MAP
    </text>

    <!-- Status Pill on right -->
    <g transform="translate(320, 24)">
        <rect width="90" height="20" rx="4" fill="#0f172a" stroke="#334155" stroke-width="1"/>
        <circle cx="12" cy="10" r="3.5" fill="#10b981" class="live-dot" />
        <text x="22" y="14" class="font-mono" font-size="10.5" fill="#94a3b8">ACTIVE</text>
    </g>

    <!-- Scanning Laser Effect -->
    <g class="scanner" transform="translate(18, 60)">
        <rect width="{width - 36}" height="28" fill="url(#laser-beam)" />
        <line x1="0" y1="28" x2="{width - 36}" y2="28" stroke="url(#laser-line)" stroke-width="1.8" />
    </g>

    <!-- Glowing Stipple Dots YG -->
    <g>
        {dots_str}
    </g>

    <!-- Footer label: model.eval() -->
    <g transform="translate({width/2}, {height - 24})">
        <text x="0" y="0" class="font-mono" font-size="13" font-weight="600" fill="#f472b6" letter-spacing="0.1em" text-anchor="middle">
            model.eval()
        </text>
    </g>
</svg>"""

    save_svg("visual_map.svg", svg)

if __name__ == "__main__":
    generate_visual_map()
