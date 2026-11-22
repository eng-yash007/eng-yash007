import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def sample_keyword_crystals(keyword: str, font, n_nodes: int, width: int = 440, height: int = 360):
    img = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(img)
    draw.text((width // 2, 185), keyword, font=font, fill=255, anchor="mm")
    
    arr = np.array(img)
    y_idx, x_idx = np.where(arr > 128)
    
    # Rejection sampling with min distance to ensure a clean molecular lattice distribution
    rng = np.random.RandomState(42)
    chosen_indices = rng.choice(len(x_idx), size=n_nodes, replace=(len(x_idx) < n_nodes))
    
    pts_x = x_idx[chosen_indices].astype(np.float32) + rng.normal(0, 1.2, n_nodes)
    pts_y = y_idx[chosen_indices].astype(np.float32) + rng.normal(0, 1.2, n_nodes)
    
    # Subtle Z depth assignment for 3D parallax
    pts_z = rng.uniform(-1.0, 1.0, n_nodes)
    
    pts = np.stack([pts_x, pts_y, pts_z], axis=1)
    
    # Sort horizontally by X for smooth, natural trajectory transitions
    order = np.argsort(pts[:, 0])
    return pts[order]

def draw_faceted_crystal(draw, x, y, size, angle, base_color, highlight_color):
    """Draws a tiny 3D faceted geometric crystal with specular glints."""
    # Rotate diamond polygon vertices
    ca = math.cos(angle)
    sa = math.sin(angle)
    
    # Local vertices: top, right, bottom, left
    rx = size * 0.72
    ry = size * 1.05
    
    vx = [-sa * (-ry), ca * rx, -sa * ry, -ca * rx]
    vy = [ca * (-ry), sa * rx, ca * ry, sa * (-rx)]
    
    p_top = (x + vx[0], y + vy[0])
    p_right = (x + vx[1], y + vy[1])
    p_bot = (x + vx[2], y + vy[2])
    p_left = (x + vx[3], y + vy[3])
    
    # Shaded Facet 1 (Left): Deeper violet / indigo tone
    facet_left_col = (
        max(int(base_color[0] * 0.65), 20),
        max(int(base_color[1] * 0.65), 30),
        max(int(base_color[2] * 0.85), 70),
        195
    )
    draw.polygon([p_top, p_left, p_bot], fill=facet_left_col)
    
    # Shaded Facet 2 (Right): Luminous iridescent cyan / pink
    facet_right_col = (
        min(int(highlight_color[0] * 1.1), 255),
        min(int(highlight_color[1] * 1.1), 255),
        min(int(highlight_color[2] * 1.1), 255),
        240
    )
    draw.polygon([p_top, p_right, p_bot], fill=facet_right_col)
    
    # Center crystal ridge line
    draw.line([p_top, p_bot], fill=(255, 255, 255, 180), width=1)
    
    # Glossy specular reflection point (top tip highlight)
    draw.point(p_top, fill=(255, 255, 255, 255))

def generate_particle_map_gif():
    width = 440
    height = 360
    n_nodes = 380
    fps = 18
    frames_per_word = 20
    
    # 4 Iconic keywords from developer profile & resume
    keywords = [
        ("GENERATIVE AI", "generative.ai"),
        ("COMPUTER VISION", "computer.vision"),
        ("MULTIMODAL AI", "multimodal.ai"),
        ("LANGCHAIN", "langchain.core")
    ]
    
    total_frames = len(keywords) * frames_per_word  # 80 frames = ~4.4s @ 18fps

    # Font setup
    try:
        font_kw = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 36)
    except Exception:
        font_kw = ImageFont.load_default()

    try:
        font_mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
    except Exception:
        font_mono = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Pre-sample crystal positions for all keywords
    word_targets = [sample_keyword_crystals(kw[0], font_kw, n_nodes, width, height) for kw in keywords]

    # Precompute individual crystal properties
    np_rng = np.random.RandomState(42)
    crystal_sizes = np_rng.uniform(2.8, 4.4, n_nodes)
    tumble_speeds = np_rng.uniform(-0.15, 0.15, n_nodes)
    initial_angles = np_rng.uniform(0, math.pi, n_nodes)
    
    # Dispersal 3D drift trajectory offsets
    drift_angles = np_rng.uniform(0, 2 * math.pi, n_nodes)
    drift_radii = np_rng.uniform(45, 120, n_nodes)
    drift_dirs = np_rng.choice([-1.0, 1.0], n_nodes)
    flutter_phase = np_rng.uniform(0, 2 * math.pi, n_nodes)

    # Iridescent scientific palette: Electric blue, cyan, iridescent violet, soft pink
    base_palette = [
        (99, 102, 241),  # indigo / electric blue
        (139, 92, 246),  # deep violet
        (168, 85, 247),  # purple
        (14, 165, 233)   # deep cyan
    ]
    
    highlight_palette = [
        (56, 189, 248),  # bright cyan
        (34, 211, 238),  # electric cyan
        (192, 132, 252), # iridescent lavender
        (244, 114, 182)  # soft pink highlight
    ]
    
    rng = random.Random(1337)
    node_base_cols = [base_palette[rng.randint(0, len(base_palette) - 1)] for _ in range(n_nodes)]
    node_high_cols = [highlight_palette[rng.randint(0, len(highlight_palette) - 1)] for _ in range(n_nodes)]

    # Pre-render static UI Frame (VISUAL.MAP)
    ui_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ui_draw = ImageDraw.Draw(ui_overlay)

    # Frame border
    ui_draw.rounded_rectangle([0, 0, width - 1, height - 1], radius=14, outline=(24, 32, 48), width=1)

    # Top bracket & label: ⌜ VISUAL.MAP
    ui_draw.line([(18, 34), (18, 18), (34, 18)], fill=(56, 189, 248), width=2)
    ui_draw.text((36, 25), "VISUAL.MAP", font=font_mono, fill=(56, 189, 248))
    ui_draw.text((width - 110, 26), "LATTICE.SYS", font=font_sub, fill=(100, 116, 139))
    
    # Horizontal divider rule
    ui_draw.line([(18, 48), (width - 18, 48)], fill=(24, 32, 48), width=1)

    # Bottom left corner bracket
    ui_draw.line([(18, height - 34), (18, height - 18), (34, height - 18)], fill=(56, 189, 248), width=2)

    # Deep matte navy background
    base_bg = Image.new("RGBA", (width, height), (6, 9, 18, 255))
    glow_draw = ImageDraw.Draw(base_bg)
    # Subtle ambient center glow
    glow_draw.ellipse([80, 110, 360, 260], fill=(16, 20, 38, 255))

    frames = []

    for f in range(total_frames):
        word_idx = f // frames_per_word
        next_word_idx = (word_idx + 1) % len(keywords)
        
        curr_t = word_targets[word_idx]
        next_t = word_targets[next_word_idx]
        local_f = f % frames_per_word
        
        # Timing curve:
        # [0..10]: Readable crystal lattice state (bonds connected, gentle 3D float)
        # [11..19]: Smooth dissolution, fluid drift & reformation into next keyword
        if local_f <= 10:
            coords = curr_t.copy()
            bonds_opacity = 1.0
            active_tag = keywords[word_idx][1]
        else:
            prog = (local_f - 10) / 10.0
            # Quintic smooth easing
            ease = prog * prog * (3.0 - 2.0 * prog)
            
            # Lattice dissolution during transition
            bonds_opacity = max(0.0, 1.0 - math.sin(prog * math.pi) * 1.4)
            
            # 3D swirl curve during morph
            arc = math.sin(prog * math.pi)
            disp_x = arc * drift_radii * np.cos(drift_angles + drift_dirs * prog * 1.8)
            disp_y = arc * drift_radii * np.sin(drift_angles + drift_dirs * prog * 1.8)
            disp_z = arc * np.sin(drift_angles * 2) * 0.8
            
            coords = (1.0 - ease) * curr_t + ease * next_t
            coords[:, 0] += disp_x
            coords[:, 1] += disp_y
            coords[:, 2] += disp_z
            active_tag = keywords[next_word_idx][1] if prog > 0.5 else keywords[word_idx][1]

        # 3D harmonic float & micro-movement
        global_t = f / float(total_frames)
        micro_x = 2.0 * np.cos(flutter_phase + 2.0 * math.pi * global_t)
        micro_y = 2.0 * np.sin(flutter_phase + 2.0 * math.pi * global_t)
        coords[:, 0] += micro_x
        coords[:, 1] += micro_y

        frame_img = base_bg.copy()
        draw = ImageDraw.Draw(frame_img, "RGBA")

        # --- PASS 1: Molecular Lattice Bonds (Filament Connections) ---
        if bonds_opacity > 0.05:
            # Pairwise distance calculation
            diff_xy = coords[:, np.newaxis, :2] - coords[np.newaxis, :, :2]
            dists = np.sqrt(np.sum(diff_xy ** 2, axis=-1))
            
            # Connect adjacent nodes within 16px
            i_idx, j_idx = np.where((dists > 4.0) & (dists < 16.5))
            for i, j in zip(i_idx, j_idx):
                if i < j:
                    d = dists[i, j]
                    # Alpha decays with distance and transition
                    alpha = int((1.0 - (d / 16.5)) * 120 * bonds_opacity)
                    if alpha > 12:
                        draw.line(
                            [(coords[i, 0], coords[i, 1]), (coords[j, 0], coords[j, 1])],
                            fill=(56, 189, 248, alpha),
                            width=1
                        )

        # --- PASS 2: Faceted Crystalline Nodes with Specular Highlights ---
        # Sort by Z-depth for 3D layering
        z_order = np.argsort(coords[:, 2])
        for i in z_order:
            px = coords[i, 0]
            py = coords[i, 1]
            pz = coords[i, 2]
            
            # Size scaled by depth perspective
            sz = crystal_sizes[i] * (1.0 + pz * 0.22)
            angle = initial_angles[i] + tumble_speeds[i] * f
            
            # Subtle refractive outer glow halo
            halo_r = sz * 1.5
            draw.ellipse(
                [px - halo_r, py - halo_r, px + halo_r, py + halo_r],
                fill=(node_high_cols[i][0], node_high_cols[i][1], node_high_cols[i][2], 38)
            )
            
            # Draw faceted crystal
            draw_faceted_crystal(draw, px, py, sz, angle, node_base_cols[i], node_high_cols[i])

        # Composite Frame UI
        frame_img.alpha_composite(ui_overlay)

        # Blinking beacon in header
        if (f % 18) < 11:
            draw.ellipse([width - 122, 28, width - 116, 34], fill=(52, 211, 153))

        # Bottom label: Knowledge Lattice Status
        footer_text = f"lattice.map // {active_tag}()"
        draw.text((width // 2, height - 26), footer_text, font=font_sub, fill=(244, 114, 182), anchor="mm")

        # Convert to paletted image with adaptive palette
        paletted = frame_img.convert("P", palette=Image.ADAPTIVE, colors=96)
        frames.append(paletted)

    out_dir = Path("assets")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "yg-particle-map.gif"
    
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True
    )
    size_kb = out_path.stat().st_size / 1024.0
    print(f"Generated crystalline molecular lattice GIF: {out_path} ({size_kb:.1f} KB, {len(frames)} frames)")

if __name__ == "__main__":
    generate_particle_map_gif()
