import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def sample_keyword_particles(word: str, font, n_word_particles: int, width: int = 440, height: int = 320):
    img = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(img)
    # Centered vertically in active zone (50..290)
    draw.text((width // 2, 162), word, font=font, fill=255, anchor="mm")
    
    arr = np.array(img)
    y_idx, x_idx = np.where(arr > 128)
    
    rng = np.random.RandomState(42)
    chosen_idx = rng.choice(len(x_idx), size=n_word_particles, replace=(len(x_idx) < n_word_particles))
    
    # Organic jitter for a rich, stippled glowing constellation
    pts_x = x_idx[chosen_idx].astype(np.float32) + rng.normal(0, 1.4, n_word_particles)
    pts_y = y_idx[chosen_idx].astype(np.float32) + rng.normal(0, 1.4, n_word_particles)
    
    pts = np.stack([pts_x, pts_y], axis=1)
    
    # Sort horizontally for smooth, non-crossing fluid morphing
    order = np.argsort(pts[:, 0])
    return pts[order]

def generate_particle_map_gif():
    # Symmetrically matched with STACK.STREAM: 440x320
    width = 440
    height = 320
    n_word_particles = 360
    n_ambient_particles = 80
    n_particles = n_word_particles + n_ambient_particles
    fps = 20
    frames_per_word = 22
    
    # Short technical keywords strictly from Yash's verified profile
    keywords = ["GenAI", "LLM", "RAG", "CV"]
    total_frames = len(keywords) * frames_per_word  # 88 frames = 4.4s @ 20fps

    # Font setup: Font size 68 gives balanced, expansive scale
    try:
        font_word = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 68)
    except Exception:
        try:
            font_word = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 68)
        except Exception:
            font_word = ImageFont.load_default()

    try:
        font_mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
        font_caption = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
    except Exception:
        font_mono = ImageFont.load_default()
        font_caption = ImageFont.load_default()

    # Pre-sample target positions for each keyword
    word_targets = [sample_keyword_particles(w, font_word, n_word_particles, width, height) for w in keywords]

    # Precompute ambient orbital particles that float gently in the outer negative space
    np_rng = np.random.RandomState(2026)
    ambient_x = np_rng.uniform(32, width - 32, n_ambient_particles)
    ambient_y = np_rng.uniform(58, height - 38, n_ambient_particles)
    ambient_targets = np.stack([ambient_x, ambient_y], axis=1)

    # Precompute dynamics
    flutter_phase = np_rng.uniform(0, 2 * math.pi, n_particles)
    flutter_speed = np_rng.uniform(1.0, 2.0, n_particles)
    flutter_amp = np_rng.uniform(0.8, 1.6, n_particles)
    
    drift_angles = np_rng.uniform(0, 2 * math.pi, n_particles)
    drift_radii = np_rng.uniform(16, 38, n_particles)
    drift_dirs = np_rng.choice([-1.0, 1.0], n_particles)

    # Curated palette matching Premium Dark Tech Design System:
    # Violet (#8B5CF6), Cyan (#22D3EE), Electric Blue (#38BDF8), Soft Pink (#F472B6)
    palette = [
        (139, 92, 246),  # Violet
        (168, 85, 247),  # Light Violet
        (34, 211, 238),  # Cyan
        (56, 189, 248),  # Electric Blue
        (99, 102, 241),  # Indigo Blue
        (244, 114, 182), # Soft Pink
        (192, 132, 252)  # Lavender
    ]
    
    rng = random.Random(42)
    colors = [palette[rng.randint(0, len(palette) - 1)] for _ in range(n_particles)]
    radii = np_rng.uniform(0.9, 1.5, n_particles)

    # Deep navy background: #080D18 -> (8, 13, 24)
    bg_color = (8, 13, 24)

    frames = []

    for f in range(total_frames):
        word_idx = f // frames_per_word
        next_word_idx = (word_idx + 1) % len(keywords)
        
        curr_t = word_targets[word_idx]
        next_t = word_targets[next_word_idx]
        local_f = f % frames_per_word
        
        # Word particles morphing
        if local_f <= 12:
            word_pos = curr_t.copy()
            bonds_opacity = 0.75
        else:
            prog = (local_f - 12) / 9.0
            ease = prog * prog * (3.0 - 2.0 * prog)
            
            arc = math.sin(prog * math.pi)
            offset_x = arc * drift_radii[:n_word_particles] * np.cos(drift_angles[:n_word_particles] + drift_dirs[:n_word_particles] * prog * 1.3)
            offset_y = arc * drift_radii[:n_word_particles] * np.sin(drift_angles[:n_word_particles] + drift_dirs[:n_word_particles] * prog * 1.3)
            
            word_pos = (1.0 - ease) * curr_t + ease * next_t
            word_pos[:, 0] += offset_x
            word_pos[:, 1] += offset_y
            bonds_opacity = max(0.0, 1.0 - arc * 1.4)

        # Ambient field particles gently breathing
        amb_pos = ambient_targets.copy()

        pos = np.vstack([word_pos, amb_pos])

        # Micro-harmonic drift
        global_t = f / float(total_frames)
        micro_x = flutter_amp * np.cos(flutter_phase + flutter_speed * 2 * math.pi * global_t)
        micro_y = flutter_amp * np.sin(flutter_phase + flutter_speed * 2 * math.pi * global_t)
        pos[:, 0] += micro_x
        pos[:, 1] += micro_y

        # Clamp safely within frame
        pos[:, 0] = np.clip(pos[:, 0], 20, width - 20)
        pos[:, 1] = np.clip(pos[:, 1], 54, height - 36)

        frame_img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(frame_img)

        # Subtle crystalline lattice filaments
        if bonds_opacity > 0.1:
            diff_xy = pos[:n_word_particles, np.newaxis, :] - pos[np.newaxis, :n_word_particles, :]
            dists = np.sqrt(np.sum(diff_xy ** 2, axis=-1))
            i_idx, j_idx = np.where((dists > 3.0) & (dists < 9.0))
            for i, j in zip(i_idx, j_idx):
                if i < j:
                    draw.line([(pos[i, 0], pos[i, 1]), (pos[j, 0], pos[j, 1])], fill=(22, 36, 62), width=1)

        # Delicate luminous particles with soft aura
        for i in range(n_particles):
            px = pos[i, 0]
            py = pos[i, 1]
            r = radii[i]
            c = colors[i]
            
            halo_c = (max(c[0] // 4, 10), max(c[1] // 4, 16), max(c[2] // 4, 30))
            draw.ellipse([px - r - 0.7, py - r - 0.7, px + r + 0.7, py + r + 0.7], fill=halo_c)
            draw.ellipse([px - r, py - r, px + r, py + r], fill=c)
            draw.point((int(px), int(py)), fill=(255, 255, 255))

        # Minimal VISUAL.MAP frame
        draw.rounded_rectangle([0, 0, width - 1, height - 1], radius=14, outline=(30, 41, 59), width=1)

        # Top-left corner bracket
        draw.line([(18, 34), (18, 18), (34, 18)], fill=(56, 189, 248), width=2)
        draw.text((38, 27), "VISUAL.MAP", font=font_mono, fill=(56, 189, 248))
        
        # Horizontal divider
        draw.line([(18, 50), (width - 18, 50)], fill=(30, 41, 59), width=1)

        # Bottom-left corner bracket
        draw.line([(18, height - 34), (18, height - 18), (34, height - 18)], fill=(56, 189, 248), width=2)

        # Bottom caption
        draw.text((width // 2, height - 20), "film.cut()", font=font_caption, fill=(244, 114, 182), anchor="mm")

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
    print(f"Generated refined VISUAL.MAP GIF: {out_path} ({size_kb:.1f} KB, {len(frames)} frames)")

if __name__ == "__main__":
    generate_particle_map_gif()
