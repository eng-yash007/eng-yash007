import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def sample_keyword_particles(word: str, font, n_particles: int, width: int = 440, height: int = 320):
    img = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(img)
    
    # Letter spacing expansion for short words so they occupy balanced horizontal scale
    display_word = word
    if len(word) == 2:
        display_word = f"{word[0]}  {word[1]}"
    elif len(word) == 3:
        display_word = f"{word[0]} {word[1]} {word[2]}"
        
    draw.text((width // 2, 165), display_word, font=font, fill=255, anchor="mm")
    
    arr = np.array(img)
    y_idx, x_idx = np.where(arr > 120)
    
    rng = np.random.RandomState(42)
    chosen_idx = rng.choice(len(x_idx), size=n_particles, replace=(len(x_idx) < n_particles))
    
    # Controlled Gaussian jitter for a luminous stippled constellation
    pts_x = x_idx[chosen_idx].astype(np.float32) + rng.normal(0, 1.3, n_particles)
    pts_y = y_idx[chosen_idx].astype(np.float32) + rng.normal(0, 1.3, n_particles)
    
    pts = np.stack([pts_x, pts_y], axis=1)
    
    # Sort horizontally for smooth fluid morphing
    order = np.argsort(pts[:, 0])
    return pts[order]

def generate_particle_map_gif():
    # Harmonious frame proportions: 440x320
    width = 440
    height = 320
    
    # 360 primary keyword particles + 64 ambient stardust particles
    n_keyword_particles = 360
    n_ambient_particles = 64
    n_total = n_keyword_particles + n_ambient_particles
    
    fps = 20
    frames_per_word = 22
    
    keywords = ["GenAI", "CV", "RAG", "LLM"]
    total_frames = len(keywords) * frames_per_word

    # Font setup: size 82 fills the viewport with clear readability
    try:
        font_word = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 82)
    except Exception:
        try:
            font_word = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 82)
        except Exception:
            font_word = ImageFont.load_default()

    try:
        font_mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
        font_caption = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
    except Exception:
        font_mono = ImageFont.load_default()
        font_caption = ImageFont.load_default()

    word_targets = [sample_keyword_particles(w, font_word, n_keyword_particles, width, height) for w in keywords]

    # Pre-generate ambient stardust positions across negative space
    np_rng = np.random.RandomState(2026)
    ambient_x = np_rng.uniform(28, width - 28, n_ambient_particles)
    ambient_y = np_rng.uniform(56, height - 36, n_ambient_particles)
    ambient_pts = np.stack([ambient_x, ambient_y], axis=1)

    # Dynamics setup
    flutter_phase = np_rng.uniform(0, 2 * math.pi, n_total)
    flutter_speed = np_rng.uniform(0.8, 1.8, n_total)
    flutter_amp = np_rng.uniform(0.6, 1.4, n_total)
    
    drift_angles = np_rng.uniform(0, 2 * math.pi, n_keyword_particles)
    drift_radii = np_rng.uniform(16, 38, n_keyword_particles)
    drift_dirs = np_rng.choice([-1.0, 1.0], n_keyword_particles)

    # Design System Palette: Electric Blue, Cyan, Violet, Soft Pink
    palette = [
        (56, 189, 248),  # electric blue
        (34, 211, 238),  # bright cyan
        (139, 92, 246),  # deep violet
        (168, 85, 247),  # vivid violet
        (192, 132, 252), # lavender
        (244, 114, 182), # soft pink
        (129, 140, 248)  # soft indigo
    ]
    
    rng = random.Random(42)
    colors = [palette[rng.randint(0, len(palette) - 1)] for _ in range(n_total)]
    
    # Delicate particle sizes: 0.9px to 1.5px
    radii = np.concatenate([
        np_rng.uniform(1.0, 1.5, n_keyword_particles),
        np_rng.uniform(0.7, 1.1, n_ambient_particles)
    ])

    bg_color = (8, 13, 24)  # #080D18

    frames = []

    for f in range(total_frames):
        word_idx = f // frames_per_word
        next_word_idx = (word_idx + 1) % len(keywords)
        
        curr_t = word_targets[word_idx]
        next_t = word_targets[next_word_idx]
        local_f = f % frames_per_word
        
        # Timing: [0..12] hold formation, [13..21] morph transition
        if local_f <= 12:
            kw_pos = curr_t.copy()
            bonds_opacity = 0.8
        else:
            prog = (local_f - 12) / 9.0
            ease = prog * prog * (3.0 - 2.0 * prog)
            
            arc = math.sin(prog * math.pi)
            offset_x = arc * drift_radii * np.cos(drift_angles + drift_dirs * prog * 1.3)
            offset_y = arc * drift_radii * np.sin(drift_angles + drift_dirs * prog * 1.3)
            
            kw_pos = (1.0 - ease) * curr_t + ease * next_t
            kw_pos[:, 0] += offset_x
            kw_pos[:, 1] += offset_y
            bonds_opacity = max(0.0, 1.0 - arc * 1.4)

        # Ambient stardust gentle drifting
        amb_pos = ambient_pts.copy()

        # Combine all particles
        all_pos = np.vstack([kw_pos, amb_pos])

        # Micro-harmonic drift
        global_t = f / float(total_frames)
        micro_x = flutter_amp * np.cos(flutter_phase + flutter_speed * 2 * math.pi * global_t)
        micro_y = flutter_amp * np.sin(flutter_phase + flutter_speed * 2 * math.pi * global_t)
        all_pos[:, 0] += micro_x
        all_pos[:, 1] += micro_y

        # Clamp safely within canvas
        all_pos[:, 0] = np.clip(all_pos[:, 0], 20, width - 20)
        all_pos[:, 1] = np.clip(all_pos[:, 1], 54, height - 38)

        frame_img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(frame_img)

        # Crystalline Filaments (subtle, delicate)
        if bonds_opacity > 0.1:
            diff_xy = kw_pos[:, np.newaxis, :] - kw_pos[np.newaxis, :, :]
            dists = np.sqrt(np.sum(diff_xy ** 2, axis=-1))
            i_idx, j_idx = np.where((dists > 3.0) & (dists < 8.5))
            for i, j in zip(i_idx, j_idx):
                if i < j:
                    draw.line([(kw_pos[i, 0], kw_pos[i, 1]), (kw_pos[j, 0], kw_pos[j, 1])], fill=(24, 38, 64), width=1)

        # Render particles
        for i in range(n_total):
            px = all_pos[i, 0]
            py = all_pos[i, 1]
            r = radii[i]
            c = colors[i]
            
            # Subtle micro halo
            halo_c = (max(c[0] // 5, 10), max(c[1] // 5, 14), max(c[2] // 5, 28))
            draw.ellipse([px - r - 0.6, py - r - 0.6, px + r + 0.6, py + r + 0.6], fill=halo_c)
            draw.ellipse([px - r, py - r, px + r, py + r], fill=c)
            
            # Specular point on primary particles
            if i < n_keyword_particles:
                draw.point((int(px), int(py)), fill=(255, 255, 255))

        # UI Frame
        draw.rounded_rectangle([0, 0, width - 1, height - 1], radius=14, outline=(30, 41, 59), width=1)

        # Top-left corner bracket
        draw.line([(18, 34), (18, 18), (34, 18)], fill=(56, 189, 248), width=2)
        draw.text((38, 25), "VISUAL.MAP", font=font_mono, fill=(56, 189, 248))
        
        # Horizontal divider line
        draw.line([(18, 48), (width - 18, 48)], fill=(30, 41, 59), width=1)

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
