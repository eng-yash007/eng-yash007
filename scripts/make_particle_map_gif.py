"""
Generates refined VISUAL.MAP GIF (440x320) strictly following the Minimal Matte Data Visualization spec:
- Completely removes all background particles, ambient stardust, and decorative noise.
- Particles are strictly confined to the centered keyword formations (GenAI, CV, RAG, LLM).
- Tiny, clean, well-defined matte dots (no outer glow, no halos, no shiny specular glints).
- Smooth, restrained, controlled morphing transitions.
- Restrained color palette: muted violet, soft blue, subtle cyan, muted pink.
"""

import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def sample_keyword_particles(word: str, font, n_particles: int, width: int = 440, height: int = 320):
    img = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(img)
    
    # Controlled tracking for short acronyms so they are clearly legible and balanced
    display_word = word
    if len(word) == 2:
        display_word = f"{word[0]}  {word[1]}"
    elif len(word) == 3:
        display_word = f"{word[0]} {word[1]} {word[2]}"
        
    draw.text((width // 2, 160), display_word, font=font, fill=255, anchor="mm")
    
    arr = np.array(img)
    y_idx, x_idx = np.where(arr > 120)
    
    rng = np.random.RandomState(42)
    chosen_idx = rng.choice(len(x_idx), size=n_particles, replace=(len(x_idx) < n_particles))
    
    # Tight, sub-pixel Gaussian placement for clean matte dots
    pts_x = x_idx[chosen_idx].astype(np.float32) + rng.normal(0, 0.7, n_particles)
    pts_y = y_idx[chosen_idx].astype(np.float32) + rng.normal(0, 0.7, n_particles)
    
    pts = np.stack([pts_x, pts_y], axis=1)
    
    # Sort horizontally for smooth, ordered morphing
    order = np.argsort(pts[:, 0])
    return pts[order]

def generate_particle_map_gif():
    # Symmetrically matched dimensions: 440x320
    width = 440
    height = 320
    
    # Strictly keyword particles only — zero background clutter
    n_particles = 320
    
    fps = 20
    frames_per_word = 22
    
    keywords = ["GenAI", "CV", "RAG", "LLM"]
    total_frames = len(keywords) * frames_per_word

    # Font setup: size 80 provides bold, crisp letter formations
    font_word = None
    for font_path in [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf"
    ]:
        try:
            font_word = ImageFont.truetype(font_path, 80)
            break
        except Exception:
            continue
    if font_word is None:
        font_word = ImageFont.load_default()

    font_mono = None
    for font_path in [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
    ]:
        try:
            font_mono = ImageFont.truetype(font_path, 12)
            break
        except Exception:
            continue
    if font_mono is None:
        font_mono = ImageFont.load_default()

    word_targets = [sample_keyword_particles(w, font_word, n_particles, width, height) for w in keywords]

    # Restrained Matte Palette: Muted violet, soft blue, subtle cyan, muted pink
    matte_palette = [
        (139, 92, 246),  # muted violet (#8B5CF6)
        (56, 189, 248),  # soft blue   (#38BDF8)
        (34, 211, 238),  # subtle cyan (#22D3EE)
        (244, 114, 182), # muted pink  (#F472B6)
        (167, 139, 250), # soft lavender (#A78BFA)
        (96, 165, 250)   # subtle cornflower (#60A5FA)
    ]
    
    rng = random.Random(42)
    colors = [matte_palette[rng.randint(0, len(matte_palette) - 1)] for _ in range(n_particles)]
    
    # Tiny, consistent matte particle radii: 1.1px to 1.4px
    np_rng = np.random.RandomState(101)
    radii = np_rng.uniform(1.1, 1.4, n_particles)
    
    # Micro-harmonic phases for organic living stippling (subtle, non-distracting)
    phases = np_rng.uniform(0, 2 * math.pi, n_particles)
    speeds = np_rng.uniform(0.6, 1.2, n_particles)

    bg_color = (8, 13, 24)  # #080D18 — clean dark navy background

    frames = []

    for f in range(total_frames):
        word_idx = f // frames_per_word
        next_word_idx = (word_idx + 1) % len(keywords)
        
        curr_t = word_targets[word_idx]
        next_t = word_targets[next_word_idx]
        local_f = f % frames_per_word
        
        # Timing: [0..13] hold static readable formation, [14..21] smooth direct morph
        if local_f <= 13:
            kw_pos = curr_t.copy()
            bonds_opacity = 1.0
        else:
            prog = (local_f - 13) / 8.0
            # Smooth cosine ease for elegant transition
            ease = 0.5 * (1.0 - math.cos(math.pi * prog))
            kw_pos = (1.0 - ease) * curr_t + ease * next_t
            bonds_opacity = max(0.0, 1.0 - math.sin(prog * math.pi) * 1.5)

        # Micro-harmonic breathing (amplitude capped at 0.4px — matte, controlled)
        global_t = f / float(total_frames)
        micro_x = 0.35 * np.cos(phases + speeds * 2 * math.pi * global_t)
        micro_y = 0.35 * np.sin(phases + speeds * 2 * math.pi * global_t)
        kw_pos[:, 0] += micro_x
        kw_pos[:, 1] += micro_y

        frame_img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(frame_img)

        # Subtle structural filaments between nearby nodes (clean generative matrix)
        if bonds_opacity > 0.1:
            diff_xy = kw_pos[:, np.newaxis, :] - kw_pos[np.newaxis, :, :]
            dists = np.sqrt(np.sum(diff_xy ** 2, axis=-1))
            i_idx, j_idx = np.where((dists > 3.0) & (dists < 6.8))
            for i, j in zip(i_idx, j_idx):
                if i < j:
                    draw.line(
                        [(kw_pos[i, 0], kw_pos[i, 1]), (kw_pos[j, 0], kw_pos[j, 1])],
                        fill=(22, 34, 56),
                        width=1
                    )

        # Render matte particles — well-defined dots, zero glow, zero specular glint
        for i in range(n_particles):
            px = kw_pos[i, 0]
            py = kw_pos[i, 1]
            r = radii[i]
            c = colors[i]
            # Solid matte disc with crisp edge
            draw.ellipse([px - r, py - r, px + r, py + r], fill=c)

        # UI Frame (strictly matches STACK.STREAM)
        draw.rounded_rectangle([0, 0, width - 1, height - 1], radius=14, outline=(30, 41, 59), width=1)

        # Top-left corner bracket
        draw.line([(18, 34), (18, 18), (34, 18)], fill=(56, 189, 248), width=2)
        draw.text((38, 25), "VISUAL.MAP", font=font_mono, fill=(56, 189, 248))
        
        # Live indicator
        draw.ellipse([(148, 19), (154, 25)], fill=(34, 211, 238))
        draw.text((160, 25), "GENERATIVE MATRIX", font=font_mono, fill=(100, 116, 139))

        # Horizontal divider line
        draw.line([(18, 48), (width - 18, 48)], fill=(30, 41, 59), width=1)

        # Bottom-left corner bracket
        draw.line([(18, height - 34), (18, height - 18), (34, height - 18)], fill=(56, 189, 248), width=2)

        # Bottom caption
        draw.text((width // 2, height - 20), "film.cut()", font=font_mono, fill=(244, 114, 182), anchor="mm")

        paletted = frame_img.quantize(colors=48, method=Image.Quantize.MEDIANCUT)
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
    print(f"Generated clean matte VISUAL.MAP GIF: {out_path} ({size_kb:.1f} KB, {len(frames)} frames)")

if __name__ == "__main__":
    generate_particle_map_gif()
