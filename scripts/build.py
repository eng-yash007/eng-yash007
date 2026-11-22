import subprocess
import sys
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def get_python_runner():
    # If sys.executable has PIL, use it; otherwise fallback to /usr/bin/python3
    try:
        import PIL
        return sys.executable
    except ImportError:
        if os.path.exists("/usr/bin/python3"):
            return "/usr/bin/python3"
        return sys.executable

def run_script(script_name: str):
    script_path = Path("scripts") / script_name
    if not script_path.exists():
        logging.warning(f"Script {script_path} not found. Skipping.")
        return
    logging.info(f"Running {script_name}...")
    runner = sys.executable
    if script_name == "make_particle_map_gif.py":
        runner = get_python_runner()
    try:
        subprocess.run([runner, str(script_path)], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run {script_name}: {e}")

def main():
    logging.info("Starting build process for modern profile...")
    
    scripts = [
        "fetch_stats.py",
        "fetch_leetcode.py",
        "make_hero_svg.py",
        "make_about_svg.py",
        "make_particle_map_gif.py",
        "make_stack_stream_svg.py",
        "make_projects_svg.py",
        "make_stats_svg.py",
        "make_social_badges.py",
        "render_heatmap.py"
    ]
    
    for script in scripts:
        run_script(script)
        
    logging.info("Build complete. All modern assets generated successfully.")

if __name__ == "__main__":
    main()
