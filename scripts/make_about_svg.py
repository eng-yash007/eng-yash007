import json
from utils import THEME, FONTS, escape, save_svg

def generate_about():
    with open("data/profile.json", "r", encoding="utf-8") as f:
        profile = json.load(f)

    college = profile.get("college", "ABES Engineering College, Ghaziabad")
    width = 900
    height = 340

    # Perfectly curated 8 core skills from Yash's Resume that fit with balanced margins
    pills = [
        "Python", "C++", "FastAPI", "LangChain", "PyTorch", "Docker", "SQL", "Git"
    ]

    # Calculate total width for perfect centering
    pill_widths = [len(p) * 8.5 + 26 for p in pills]
    gap = 12
    total_pills_width = sum(pill_widths) + gap * (len(pills) - 1)
    start_x = (width - total_pills_width) / 2
    pill_y = 284

    pill_elements = []
    curr_x = start_x
    for pill, pw in zip(pills, pill_widths):
        pill_elements.append(f"""
        <g transform="translate({curr_x:.1f}, {pill_y})">
            <rect width="{pw:.1f}" height="28" rx="14" fill="#0f172a" fill-opacity="0.85" stroke="#334155" stroke-width="1"/>
            <text x="{pw/2:.1f}" y="18" fill="#e2e8f0" font-size="12" font-weight="500" class="font-sans" text-anchor="middle">
                {escape(pill)}
            </text>
        </g>
        """)
        curr_x += pw + gap

    pills_markup = "\n".join(pill_elements)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="about-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#080c14" />
            <stop offset="60%" stop-color="#0b101d" />
            <stop offset="100%" stop-color="#070a12" />
        </linearGradient>

        <linearGradient id="card-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0f172a" stop-opacity="0.9" />
            <stop offset="100%" stop-color="#060911" stop-opacity="0.9" />
        </linearGradient>

        <linearGradient id="about-border" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1e293b" stop-opacity="0.9"/>
            <stop offset="50%" stop-color="#334155" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#1e293b" stop-opacity="0.9"/>
        </linearGradient>
    </defs>

    <style>
        .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif; }}
        .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, Menlo, monospace; }}
    </style>

    <!-- Background Container -->
    <rect width="{width}" height="{height}" rx="14" fill="url(#about-bg)" />
    <rect width="{width}" height="{height}" rx="14" fill="none" stroke="url(#about-border)" stroke-width="1.2" />

    <!-- Top Tag -->
    <g transform="translate(36, 26)">
        <rect width="180" height="22" rx="4" fill="#1e293b" fill-opacity="0.6"/>
        <text x="90" y="15" fill="#818cf8" font-size="11" font-weight="600" class="font-mono" text-anchor="middle">
            PROFILE // SPECIFICATION
        </text>
    </g>

    <!-- LEFT COLUMN: Introduction -->
    <g transform="translate(36, 68)">
        <text x="0" y="28" class="font-sans" font-size="28" font-weight="800" fill="#f8fafc">
            Yash Gupta
        </text>

        <text x="0" y="52" class="font-sans" font-size="13" font-weight="600" fill="#2dd4bf">
            Generative AI Engineer | LLMs &amp; RAG Systems
        </text>

        <text x="0" y="74" class="font-sans" font-size="12.5" font-weight="500" fill="#94a3b8">
            {escape(college)} · CGPA 8.0
        </text>

        <!-- Concise, Resume-aligned Paragraph -->
        <text x="0" y="104" class="font-sans" font-size="13" fill="#94a3b8" line-height="1.5">
            <tspan x="0" dy="0">Computer Science (Data Science) undergraduate engineer</tspan>
            <tspan x="0" dy="20">passionate about building production-grade GenAI pipelines.</tspan>
            <tspan x="0" dy="20">Hands-on experience with real-time CV workflows at Ragh Vision</tspan>
            <tspan x="0" dy="20">and enterprise RAG chatbots &amp; analytics at Capri Global.</tspan>
        </text>
    </g>

    <!-- RIGHT COLUMN: Terminal Identity Card (Zero Overflow Guaranteed) -->
    <g transform="translate(485, 32)">
        <rect width="380" height="228" rx="12" fill="url(#card-grad)" stroke="#1e293b" stroke-width="1.1"/>

        <!-- Terminal Title Bar -->
        <g transform="translate(16, 18)">
            <circle cx="0" cy="0" r="4.5" fill="#ff5f56"/>
            <circle cx="14" cy="0" r="4.5" fill="#ffbd2e"/>
            <circle cx="28" cy="0" r="4.5" fill="#27c93f"/>
            <text x="44" y="4" class="font-mono" font-size="11" fill="#64748b" font-weight="600">
                # yash.config
            </text>
        </g>

        <!-- Terminal Content -->
        <g transform="translate(18, 54)">
            <!-- identity -->
            <text x="0" y="0" class="font-mono" font-size="12">
                <tspan fill="#2dd4bf">identity</tspan><tspan fill="#64748b">: </tspan><tspan fill="#f1f5f9">"Generative AI Engineer"</tspan>
            </text>

            <!-- focus -->
            <text x="0" y="26" class="font-mono" font-size="12">
                <tspan fill="#2dd4bf">focus</tspan><tspan fill="#64748b">: [</tspan><tspan fill="#f1f5f9">"GenAI"</tspan><tspan fill="#64748b">, </tspan><tspan fill="#f1f5f9">"LLMs"</tspan><tspan fill="#64748b">, </tspan><tspan fill="#f1f5f9">"RAG Systems"</tspan><tspan fill="#64748b">]</tspan>
            </text>

            <!-- experience -->
            <text x="0" y="52" class="font-mono" font-size="12">
                <tspan fill="#2dd4bf">experience</tspan><tspan fill="#64748b">: [</tspan><tspan fill="#f1f5f9">"Capri Global"</tspan><tspan fill="#64748b">, </tspan><tspan fill="#f1f5f9">"Ragh Vision"</tspan><tspan fill="#64748b">]</tspan>
            </text>

            <!-- core_stack (clean, concise, zero overflow) -->
            <text x="0" y="78" class="font-mono" font-size="12">
                <tspan fill="#2dd4bf">core_stack</tspan><tspan fill="#64748b">: [</tspan><tspan fill="#f1f5f9">"Python"</tspan><tspan fill="#64748b">, </tspan><tspan fill="#f1f5f9">"FastAPI"</tspan><tspan fill="#64748b">, </tspan><tspan fill="#f1f5f9">"LangChain"</tspan><tspan fill="#64748b">]</tspan>
            </text>

            <!-- status -->
            <text x="0" y="104" class="font-mono" font-size="12">
                <tspan fill="#2dd4bf">status</tspan><tspan fill="#64748b">: </tspan><tspan fill="#34d399">"eager to build real-world AI systems"</tspan>
            </text>
        </g>
    </g>

    <!-- BOTTOM ROW: Centered Tech Badges -->
    {pills_markup}
</svg>"""

    save_svg("about.svg", svg)

if __name__ == "__main__":
    generate_about()
