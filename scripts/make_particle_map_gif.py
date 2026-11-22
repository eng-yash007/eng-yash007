import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def sample_keyword_particles(word: str, font, n_particles: int, width: int = 440, height: int = 360):
    img = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(img)
    draw.text((width // 2, 182), word, font=font, fill=255, anchor="mm")
    
    arr = np.array(img)
    y_idx, x_idx = np.where(arr > 128)
    
    rng = np.random.RandomState(42)
    chosen_idx = rng.choice(len(x_idx), size=n_particles, replace=(len(x_idx) < n_particles))
    
    pts_x = x_idx[chosen_idx].astype(np.float32) + rng.normal(0, 1.2, n_particles)
    pts_y = y_idx[chosen_idx].astype(np.float32) + rng.normal(0, 1.2, n_particles)
    
    pts = np.stack([pts_x, pts_y], axis=1)
    
    # Sort horizontally for smooth, non-crossing fluid morphing
    order = np.argsort(pts[:, 0])
    return pts[order]

def generate_particle_map_gif():
    width = 440
    height = 360
    n_particles = 320
    fps = 20
    frames_per_word = 22
    
    # Short technical keywords strictly from the user's list
    keywords = ["GenAI", "CV", "RAG", "LLM"]
    total_frames = len(keywords) * frames_per_word  # 88 frames = 4.4s @ 20fps

    # Font setup
    try:
        font_word = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 44)
    except Exception:
        font_word = ImageFont.load_default()

    try:
        font_mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
        font_caption = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
    except Exception:
        font_mono = ImageFont.load_default()
        font_caption = ImageFont.load_default()

    # Pre-sample target positions for each keyword
    word_targets = [sample_keyword_particles(w, font_word, n_particles, width, height) for w in keywords]

    # Precompute subtle floating and morphing dynamics
    np_rng = np.random.RandomState(2026)
    flutter_phase = np_rng.uniform(0, 2 * math.pi, n_particles)
    flutter_speed = np_rng.uniform(1.2, 2.2, n_particles)
    flutter_amp = np_rng.uniform(1.2, 2.5, n_particles)
    
    # Controlled, gentle drift offsets during transition (contained within frame)
    drift_angles = np_rng.uniform(0, 2 * math.pi, n_particles)
    drift_radii = np_rng.uniform(20, 50, n_particles)  # Gentle distance, no frame overflow
    drift_dirs = np_rng.choice([-1.0, 1.0], n_particles)

    # Strictly curated palette:
    # Primary: Violet, Electric Blue
    # Secondary: Soft Pink, Cyan, Lavender
    # ABSOLUTELY NO RED, NO GREEN, NO YELLOW
    palette = [
        (168, 85, 247),  # violet
        (139, 92, 246),  # deep violet
        (99, 102, 241),  # electric blue
        (129, 140, 248), # soft indigo
        (56, 189, 248),  # cyan
        (34, 211, 238),  # bright cyan
        (244, 114, 182), # soft pink
        (192, 132, 252)  # lavender
    ]
    
    rng = random.Random(42)
    colors = [palette[rng.randint(0, len(palette) - 1)] for _ in range(n_particles)]
    
    # Tiny, delicate particle sizes: 1.6px to 2.4px
    radii = np_rng.uniform(1.6, 2.5, n_particles)

    # Static clean UI Frame (Exact matching of original reference image)
    # Background: pure uniform dark navy (7, 10, 19). No background blobs.
    bg_color = (7, 10, 19)

    frames = []

    for f in range(total_frames):
        word_idx = f // frames_per_word
        next_word_idx = (word_idx + 1) % len(keywords)
        
        curr_t = word_targets[word_idx]
        next_t = word_targets[next_word_idx]
        local_f = f % frames_per_word
        
        # Timing:
        # [0..12]: Stable, highly readable formation with gentle floating
        # [13..21]: Smooth, elegant dissolution and morph into next keyword
        if local_f <= 12:
            pos = curr_t.copy()
            bonds_opacity = 0.8
        else:
            prog = (local_f - 12) / 9.0
            # Smooth cubic easing
            ease = prog * prog * (3.0 - 2.0 * prog)
            
            # Gentle curved swirl offset during morph (smooth arc)
            arc = math.sin(prog * math.pi)
            offset_x = arc * drift_radii * np.cos(drift_angles + drift_dirs * prog * 1.4)
            offset_y = arc * drift_radii * np.sin(drift_angles + drift_dirs * prog * 1.4)
            
            pos = (1.0 - ease) * curr_t + ease * next_t
            pos[:, 0] += offset_x
            pos[:, 1] += offset_y
            bonds_opacity = max(0.0, 1.0 - arc * 1.3)

        # Micro-harmonic drift (natural breathing movement)
        global_t = f / float(total_frames)
        micro_x = flutter_amp * np.cos(flutter_phase + flutter_speed * 2 * math.pi * global_t)
        micro_y = flutter_amp * np.sin(flutter_phase + flutter_speed * 2 * math.pi * global_t)
        pos[:, 0] += micro_x
        pos[:, 1] += micro_y

        # Clamp positions safely within canvas margins
        pos[:, 0] = np.clip(pos[:, 0], 28, width - 28)
        pos[:, 1] = np.clip(pos[:, 1], 65, height - 48)

        # Create clean RGB frame (No buggy RGBA compositing)
        frame_img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(frame_img)

        # --- Delicate Crystalline Connections (Filaments) ---
        if bonds_opacity > 0.1:
            diff_xy = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
            dists = np.sqrt(np.sum(diff_xy ** 2, axis=-1))
            i_idx, j_idx = np.where((dists > 3.0) & (dists < 10.5))
            for i, j in zip(i_idx, j_idx):
                if i < j:
                    # Soft blend color: mix cyan and background
                    line_col = (28, 48, 80)
                    draw.line([(pos[i, 0], pos[i, 1]), (pos[j, 0], pos[j, 1])], fill=line_col, width=1)

        # --- Tiny Luminous Particles with Specular Highlight ---
        for i in range(n_particles):
            px = pos[i, 0]
            py = pos[i, 1]
            r = radii[i]
            c = colors[i]
            
            # Subtle outer glow halo (tiny, radius + 1px)
            halo_c = (max(c[0] // 4, 15), max(c[1] // 4, 20), max(c[2] // 4, 40))
            draw.ellipse([px - r - 1.0, py - r - 1.0, px + r + 1.0, py + r + 1.0], fill=halo_c)
            
            # Particle luminous core
            draw.ellipse([px - r, py - r, px + r, py + r], fill=c)
            
            # Tiny crystal specular highlight glint
            draw.point((int(px), int(py)), fill=(255, 255, 255))

        # --- UI Frame (Preserving original minimal VISUAL.MAP frame) ---
        # Outer thin border
        draw.rounded_rectangle([0, 0, width - 1, height - 1], radius=14, outline=(24, 32, 47), width=1)

        # Top-left corner bracket
        draw.line([(18, 34), (18, 18), (34, 18)], fill=(56, 189, 248), width=2)
        draw.text((36, 26), "VISUAL.MAP", font=font_mono, fill=(56, 189, 248))
        
        # Horizontal thin divider line
        draw.line([(18, 48), (width - 18, 48)], fill=(24, 32, 47), width=1)

        # Bottom-left corner bracket
        draw.line([(18, height - 34), (18, height - 18), (34, height - 18)], fill=(56, 189, 248), width=2)

        # Small bottom caption: film.cut() in soft pink (exact reference styling)
        draw.text((width // 2, height - 28), "film.cut()", font=font_caption, fill=(244, 114, 182), anchor="mm")

        # Quantize cleanly using median-cut on RGB with 64 colors
        paletted = frame_img.quantize(colors=64, method=Image.Quantize.MEDIANCUT)
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
    print(f"Generated clean refined particle map GIF: {out_path} ({size_kb:.1f} KB, {len(frames)} frames)")

if __name__ == "__main__":
    generate_particle_map_gif()
