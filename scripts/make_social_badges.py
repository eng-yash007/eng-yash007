from pathlib import Path
from utils import FONTS, escape, save_svg

def create_badge(name, handle, icon_path, brand_color, glow_color, filename):
    width = 175
    height = 42

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0b101c" />
            <stop offset="100%" stop-color="#050811" />
        </linearGradient>

        <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{brand_color}" stop-opacity="0.8" />
            <stop offset="50%" stop-color="{glow_color}" stop-opacity="0.3" />
            <stop offset="100%" stop-color="{brand_color}" stop-opacity="0.7" />
        </linearGradient>

        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
    </defs>

    <style>
        .font-sans {{ font-family: {FONTS['sans']}; }}
        .font-mono {{ font-family: {FONTS['mono']}; }}

        @keyframes badgePulse {{
            0%, 100% {{
                stroke-opacity: 0.6;
            }}
            50% {{
                stroke-opacity: 1;
                filter: drop-shadow(0 0 4px {glow_color});
            }}
        }}

        @keyframes dotGlow {{
            0%, 100% {{ r: 3px; opacity: 0.8; }}
            50% {{ r: 4.5px; opacity: 1; }}
        }}

        .card-border {{
            animation: badgePulse 3s infinite ease-in-out;
        }}
        .live-dot {{
            animation: dotGlow 2s infinite ease-in-out;
        }}
    </style>

    <!-- Pill Container -->
    <rect width="{width}" height="{height}" rx="21" fill="url(#bg-grad)" />
    <rect width="{width}" height="{height}" rx="21" fill="none" stroke="url(#border-grad)" stroke-width="1.3" class="card-border" />

    <!-- Icon on Left -->
    <g transform="translate(14, 11)">
        {icon_path}
    </g>

    <!-- Text details -->
    <text x="44" y="19" class="font-sans" font-size="11.5" font-weight="700" fill="#f8fafc">
        {escape(name)}
    </text>
    <text x="44" y="32" class="font-mono" font-size="10" font-weight="500" fill="#94a3b8">
        {escape(handle)}
    </text>

    <!-- Right Live Dot -->
    <circle cx="{width - 16}" cy="21" r="3.5" fill="{brand_color}" class="live-dot" />
</svg>"""

    save_svg(filename, svg)

def generate_all_badges():
    # 1. GitHub
    github_icon = """<path fill="#e2e8f0" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z"/>"""
    create_badge("GitHub", "eng-yash007", github_icon, "#818cf8", "#c084fc", "badge_github.svg")

    # 2. LinkedIn
    linkedin_icon = """<path fill="#0ea5e9" d="M19 0h-18c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1v-18c0-.55-.45-1-1-1zm-11 17h-3v-9h3v9zm-1.5-10.27c-.97 0-1.75-.79-1.75-1.76s.78-1.75 1.75-1.75 1.75.78 1.75 1.75-.78 1.76-1.75 1.76zm11.5 10.27h-3v-4.6c0-1.1-.02-2.52-1.54-2.52-1.54 0-1.78 1.2-1.78 2.44v4.68h-3v-9h2.88v1.23h.04c.4-.76 1.38-1.56 2.84-1.56 3.04 0 3.6 2 3.6 4.6v4.73z"/>"""
    create_badge("LinkedIn", "eng-yash007", linkedin_icon, "#0ea5e9", "#38bdf8", "badge_linkedin.svg")

    # 3. LeetCode
    leetcode_icon = """<path fill="#fbbf24" d="M13.483 0a1.374 1.374 0 00-.961.438L7.116 6.226l-3.854 4.126a5.266 5.266 0 00-1.209 2.104 5.35 5.35 0 00-.125.513 5.527 5.527 0 00.271 4.735 5.32 5.32 0 004.126 2.671 5.362 5.362 0 004.604-1.583l4.558-4.882a1.376 1.376 0 00-.02-1.921 1.376 1.376 0 00-1.921.02L9.127 16.9a2.604 2.604 0 01-2.24 1.042 2.604 2.604 0 01-2.01-1.302 2.698 2.698 0 01-.135-2.312c.135-.375.354-.708.646-.979l4.558-4.882 4.412-4.72a1.376 1.376 0 00-.875-2.747z"/><path fill="#f59e0b" d="M9.833 10.979h8.334a1.375 1.375 0 000-2.75H9.833a1.375 1.375 0 000 2.75z"/>"""
    create_badge("LeetCode", "eng-yash007", leetcode_icon, "#f59e0b", "#fbbf24", "badge_leetcode.svg")

    # 4. CodeChef
    codechef_icon = """<path fill="#f97316" d="M10 2a8 8 0 108 8 8.009 8.009 0 00-8-8zm0 14a6 6 0 116-6 6.007 6.007 0 01-6 6zm1-9H9v4h2zm0 6H9v2h2z"/>"""
    create_badge("CodeChef", "yashgupta9171", codechef_icon, "#f97316", "#fb923c", "badge_codechef.svg")

    # 5. Email
    email_icon = """<path fill="#f43f5e" d="M1.5 4.5A2.5 2.5 0 014 2h12a2.5 2.5 0 012.5 2.5v11a2.5 2.5 0 01-2.5 2.5H4a2.5 2.5 0 01-2.5-2.5v-11zm2.75.5L10 9.75 15.75 5H4.25zM17 6.35l-6.53 5.37a.75.75 0 01-.94 0L3 6.35V15.5c0 .414.336.75.75.75h12.5a.75.75 0 00.75-.75V6.35z"/>"""
    create_badge("Email", "Direct Connect", email_icon, "#f43f5e", "#fb7185", "badge_email.svg")

if __name__ == "__main__":
    generate_all_badges()

