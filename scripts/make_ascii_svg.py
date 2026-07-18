from PIL import Image
from utils import COLORS, FONTS, save_svg
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Character ramp from darkest to lightest
ASCII_CHARS = " .`:-=+*#%@"

def resize_image(image, new_width=60):
    width, height = image.size
    # Adjust aspect ratio for terminal fonts (typically 1:2 width to height)
    aspect_ratio = height / width / 1.65 
    new_height = int(aspect_ratio * new_width)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        # map pixel value 0-255 to ascii chars
        idx = int(pixel / 255 * (len(ASCII_CHARS) - 1))
        ascii_str += ASCII_CHARS[idx]
    return ascii_str

def generate_ascii_svg():
    input_path = Path("data/processed_photo.png")
    if not input_path.exists():
        logging.warning(f"{input_path} not found. Run prep_photo.py first.")
        # Fallback dummy ascii
        lines = [
            "  .----------------.  ",
            " | .--------------. | ",
            " | |  YASH GUPTA  | | ",
            " | |              | | ",
            " | |  AI ENGINEER | | ",
            " | '--------------' | ",
            "  '----------------'  "
        ]
    else:
        try:
            image = Image.open(input_path).convert('L')
            image = resize_image(image, new_width=50)
            ascii_str = pixels_to_ascii(image)
            
            img_width = image.width
            ascii_str_len = len(ascii_str)
            lines = [ascii_str[index: index + img_width] for index in range(0, ascii_str_len, img_width)]
        except Exception as e:
            logging.error(f"Error converting to ASCII: {e}")
            return
            
    # SVG styling for terminal typing effect
    svg_width = 350
    svg_height = 400
    
    title_bar = f"""
    <rect width="100%" height="30" fill="{COLORS['border']}" rx="4" />
    <circle cx="15" cy="15" r="6" fill="#ff5f56"/>
    <circle cx="35" cy="15" r="6" fill="#ffbd2e"/>
    <circle cx="55" cy="15" r="6" fill="#27c93f"/>
    <text x="50%" y="20" class="text-primary" font-size="14" text-anchor="middle">yash@github: ~/portrait</text>
    """
    
    ascii_svg = ""
    delay = 0.5
    for i, line in enumerate(lines):
        # Escape special XML chars if any
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        ascii_svg += f"""
        <g class="fade-in" style="animation-delay: {delay}s; opacity: 0;">
            <text x="20" y="{60 + i * 12}" font-size="10" class="text-accent" xml:space="preserve">{safe_line}</text>
        </g>
        """
        delay += 0.05  # Fast typing effect line by line

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
    <style>
        .text-primary {{ font-family: {FONTS['primary']}; fill: {COLORS['primary']}; }}
        .text-accent {{ font-family: {FONTS['primary']}; fill: {COLORS['accent']}; font-weight: bold; letter-spacing: 1px; }}
        .bg {{ fill: {COLORS['background']}; }}
        .border {{ stroke: {COLORS['border']}; fill: none; }}
        
        @keyframes fadeInSlide {{
            0% {{ opacity: 0; transform: translateY(-5px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        .fade-in {{
            animation: fadeInSlide 0.2s forwards ease-out;
        }}
    </style>
    
    <rect width="{svg_width}" height="{svg_height}" class="bg" rx="6" />
    <rect width="{svg_width}" height="{svg_height}" class="border" rx="6" stroke-width="2"/>
    
    {title_bar}
    {ascii_svg}
</svg>"""

    save_svg("ascii.svg", svg_content)

if __name__ == "__main__":
    generate_ascii_svg()
