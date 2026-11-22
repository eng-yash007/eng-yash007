from pathlib import Path
from utils import FONTS, escape, save_svg

def create_badge(name, handle, icon_path, brand_color, glow_color, filename):
    # Compact width 132x34 to guarantee 100% single-row non-wrapping on all screens
    width = 132
    height = 34

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="bg-grad-{name.lower()}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0d1322" />
            <stop offset="100%" stop-color="#060912" />
        </linearGradient>

        <linearGradient id="border-grad-{name.lower()}" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{brand_color}" stop-opacity="0.8" />
            <stop offset="50%" stop-color="{glow_color}" stop-opacity="0.25" />
            <stop offset="100%" stop-color="{brand_color}" stop-opacity="0.6" />
        </linearGradient>
    </defs>

    <style>
        .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; }}

        @keyframes badgePulse {{
            0%, 100% {{ stroke-opacity: 0.5; }}
            50% {{ stroke-opacity: 0.95; }}
        }}
        @keyframes dotGlow {{
            0%, 100% {{ r: 2.2px; opacity: 0.6; }}
            50% {{ r: 3.2px; opacity: 1; }}
        }}

        .card-border {{
            animation: badgePulse 3s infinite ease-in-out;
        }}
        .live-dot {{
            animation: dotGlow 2s infinite ease-in-out;
        }}
    </style>

    <!-- Pill Container -->
    <rect width="{width}" height="{height}" rx="17" fill="url(#bg-grad-{name.lower()})" />
    <rect width="{width}" height="{height}" rx="17" fill="none" stroke="url(#border-grad-{name.lower()})" stroke-width="1.1" class="card-border" />

    <!-- Icon on Left -->
    <g transform="translate(10, 8.5) scale(0.85)">
        {icon_path}
    </g>

    <!-- Text details -->
    <text x="32" y="15" class="font-sans" font-size="10.5" font-weight="700" fill="#f8fafc">
        {escape(name)}
    </text>
    <text x="32" y="26" class="font-mono" font-size="8" font-weight="500" fill="#94a3b8">
        {escape(handle)}
    </text>

    <!-- Live indicator on Right -->
    <circle cx="{width - 12}" cy="17" r="2.5" fill="{brand_color}" class="live-dot" />
</svg>"""

    save_svg(filename, svg)

def generate_all_badges():
    # Icons
    github_icon = """<path fill="#f8fafc" d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>"""

    linkedin_icon = """<path fill="#0a66c2" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>"""

    leetcode_icon = """<path fill="#ffa116" d="M13.483 0a1.374 1.374 0 0 0-.961.438L7.116 6.226l-3.854 4.126a5.266 5.266 0 0 0-1.209 2.104 5.35 5.35 0 0 0-.125.513 5.527 5.527 0 0 0 .062 2.362 5.83 5.83 0 0 0 .349 1.017 5.938 5.938 0 0 0 1.271 1.818l4.277 4.193.039.038c2.248 2.165 5.852 2.133 8.063-.074l2.396-2.392c.54-.54.54-1.414.003-1.955a1.378 1.378 0 0 0-1.951-.003l-2.396 2.392a3.021 3.021 0 0 1-4.205.038l-.02-.019-4.276-4.193c-.652-.64-.972-1.469-.948-2.263a2.68 2.68 0 0 1 .066-.523 2.545 2.545 0 0 1 .619-1.164L9.13 8.114c1.058-1.134 3.204-1.27 4.43-.278l3.501 2.831c.593.48 1.461.387 1.94-.207a1.384 1.384 0 0 0-.207-1.943l-3.5-2.831c-2.42-1.955-5.918-1.632-7.811.458z"/>"""

    codechef_icon = """<path fill="#ea580c" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>"""

    email_icon = """<path fill="#ec4899" d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>"""

    create_badge("GitHub", "eng-yash007", github_icon, "#818cf8", "#38bdf8", "assets/badge_github.svg")
    create_badge("LinkedIn", "eng-yash007", linkedin_icon, "#0a66c2", "#38bdf8", "assets/badge_linkedin.svg")
    create_badge("LeetCode", "eng-yash007", leetcode_icon, "#ffa116", "#fbbf24", "assets/badge_leetcode.svg")
    create_badge("CodeChef", "yashgupta9171", codechef_icon, "#ea580c", "#f97316", "assets/badge_codechef.svg")
    create_badge("Email", "Direct Connect", email_icon, "#ec4899", "#f472b6", "assets/badge_email.svg")

if __name__ == "__main__":
    generate_all_badges()
