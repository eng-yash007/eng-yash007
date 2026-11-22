import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def sample_keyword_particles(word: str, font, n_particles: int, width: int = 440, height: int = 480):
    img = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(img)
    # Perfectly centered in the expanded vertical canvas
    draw.text((width // 2, 245), word, font=font, fill=255, anchor="mm")
    
    arr = np.array(img)
    y_idx, x_idx = np.where(arr > 128)
    
    rng = np.random.RandomState(42)
    chosen_idx = rng.choice(len(x_idx), size=n_particles, replace=(len(x_idx) < n_particles))
    
    # Slight organic jitter to mimic the natural stippled particle constellation
    pts_x = x_idx[chosen_idx].astype(np.float32) + rng.normal(0, 1.2, n_particles)
    pts_y = y_idx[chosen_idx].astype(np.float32) + rng.normal(0, 1.2, n_particles)
    
    pts = np.stack([pts_x, pts_y], axis=1)
    
    # Sort horizontally for smooth, non-crossing fluid morphing
    order = np.argsort(pts[:, 0])
    return pts[order]

def generate_particle_map_gif():
    # Overall increased canvas size: 440x480 for a grand, tall, elegant card
    width = 440
    height = 480
    n_particles = 480  # Denser starry particle cloud
    fps = 20
    frames_per_word = 22
    
    # Short technical keywords strictly from the user's verified profile
    keywords = ["GenAI", "CV", "RAG", "LLM"]
    total_frames = len(keywords) * frames_per_word  # 88 frames = 4.4s @ 20fps

    # Font setup
    try:
        font_word = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 54)
    except Exception:
        try:
            font_word = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 54)
        except Exception:
            font_word = ImageFont.load_default()

    try:
        font_mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
        font_caption = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
    except Exception:
        font_mono = ImageFont.load_default()
        font_caption = ImageFont.load_default()

    # Pre-sample target positions for each keyword
    word_targets = [sample_keyword_particles(w, font_word, n_particles, width, height) for w in keywords]

    # Precompute subtle floating and morphing dynamics
    np_rng = np.random.RandomState(2026)
    flutter_phase = np_rng.uniform(0, 2 * math.pi, n_particles)
    flutter_speed = np_rng.uniform(1.0, 2.0, n_particles)
    flutter_amp = np_rng.uniform(0.8, 1.8, n_particles)
    
    # Controlled gentle drift offsets during transition (contained within frame)
    drift_angles = np_rng.uniform(0, 2 * math.pi, n_particles)
    drift_radii = np_rng.uniform(20, 50, n_particles)
    drift_dirs = np_rng.choice([-1.0, 1.0], n_particles)

    # Reference-accurate Palette:
    # Luminous soft pink, magenta, violet, electric blue, cyan, lavender
    palette = [
        (244, 114, 182), # soft pink
        (251, 113, 133), # coral rose
        (232, 121, 249), # neon fuchsia
        (192, 132, 252), # lavender
        (168, 85, 247),  # vivid violet
        (139, 92, 246),  # deep violet
        (99, 102, 241),  # electric indigo
        (56, 189, 248),  # sky cyan
        (34, 211, 238),  # bright cyan
    ]
    
    rng = random.Random(42)
    colors = [palette[rng.randint(0, len(palette) - 1)] for _ in range(n_particles)]
    
    # SMALL, DELICATE PARTICLE SIZES: 0.9px to 1.5px (as requested by user)
    radii = np_rng.uniform(0.9, 1.5, n_particles)

    # Pure uniform dark navy background (zero red blob, zero background artifacts)
    bg_color = (7, 10, 19)

    frames = []

    for f in range(total_frames):
        word_idx = f // frames_per_word
        next_word_idx = (word_idx + 1) % len(keywords)
        
        curr_t = word_targets[word_idx]
        next_t = word_targets[next_word_idx]
        local_f = f % frames_per_word
        
        # Timing:
        # [0..12]: Stable, highly readable formation with gentle micro-floating
        # [13..21]: Smooth, elegant dissolution and morph into next keyword
        if local_f <= 12:
            pos = curr_t.copy()
            bonds_opacity = 0.8
        else:
            prog = (local_f - 12) / 9.0
            # Smooth cubic easing
            ease = prog * prog * (3.0 - 2.0 * prog)
            
            # Gentle curved swirl offset during morph
            arc = math.sin(prog * math.pi)
            offset_x = arc * drift_radii * np.cos(drift_angles + drift_dirs * prog * 1.3)
            offset_y = arc * drift_radii * np.sin(drift_angles + drift_dirs * prog * 1.3)
            
            pos = (1.0 - ease) * curr_t + ease * next_t
            pos[:, 0] += offset_x
            pos[:, 1] += offset_y
            bonds_opacity = max(0.0, 1.0 - arc * 1.4)

        # Micro-harmonic drift (natural living motion)
        global_t = f / float(total_frames)
        micro_x = flutter_amp * np.cos(flutter_phase + flutter_speed * 2 * math.pi * global_t)
        micro_y = flutter_amp * np.sin(flutter_phase + flutter_speed * 2 * math.pi * global_t)
        pos[:, 0] += micro_x
        pos[:, 1] += micro_y

        # Clamp positions safely within canvas margins
        pos[:, 0] = np.clip(pos[:, 0], 24, width - 24)
        pos[:, 1] = np.clip(pos[:, 1], 66, height - 52)

        # Create clean RGB frame
        frame_img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(frame_img)

        # --- Delicate Crystalline Connections (Filaments) ---
        if bonds_opacity > 0.1:
            diff_xy = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
            dists = np.sqrt(np.sum(diff_xy ** 2, axis=-1))
            i_idx, j_idx = np.where((dists > 3.0) & (dists < 9.0))
            for i, j in zip(i_idx, j_idx):
                if i < j:
                    line_col = (24, 38, 68)
                    draw.line([(pos[i, 0], pos[i, 1]), (pos[j, 0], pos[j, 1])], fill=line_col, width=1)

        # --- Tiny Luminous Delicate Particles with Micro-Halo and Specular Core ---
        for i in range(n_particles):
            px = pos[i, 0]
            py = pos[i, 1]
            r = radii[i]
            c = colors[i]
            
            # Subtle micro halo (subtle glow)
            halo_c = (max(c[0] // 4, 12), max(c[1] // 4, 16), max(c[2] // 4, 32))
            draw.ellipse([px - r - 0.7, py - r - 0.7, px + r + 0.7, py + r + 0.7], fill=halo_c)
            
            # Particle luminous core
            draw.ellipse([px - r, py - r, px + r, py + r], fill=c)
            
            # Tiny crystal specular highlight point
            draw.point((int(px), int(py)), fill=(255, 255, 255))

        # --- UI Frame (Minimal VISUAL.MAP frame matching reference exactly) ---
        # Outer thin border
        draw.rounded_rectangle([0, 0, width - 1, height - 1], radius=14, outline=(24, 32, 47), width=1)

        # Top-left corner bracket
        draw.line([(18, 36), (18, 18), (36, 18)], fill=(56, 189, 248), width=2)
        draw.text((40, 27), "VISUAL.MAP", font=font_mono, fill=(56, 189, 248))
        
        # Horizontal thin divider line
        draw.line([(18, 52), (width - 18, 52)], fill=(24, 32, 47), width=1)

        # Bottom-left corner bracket
        draw.line([(18, height - 36), (18, height - 18), (36, height - 18)], fill=(56, 189, 248), width=2)

        # Small bottom caption: film.cut() in soft pink (matching user reference)
        draw.text((width // 2, height - 28), "film.cut()", font=font_caption, fill=(244, 114, 182), anchor="mm")

        # Quantize cleanly using median-cut on RGB (no color drift)
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
    print(f"Generated enlarged refined particle map GIF: {out_path} ({size_kb:.1f} KB, {len(frames)} frames)")

if __name__ == "__main__":
    generate_particle_map_gif()
