"""
Master Build Script: Orchestrates live data fetching and SVG/GIF asset generation.
"""

import subprocess
import sys
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def get_python_runner():
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
    logging.info(f"Executing {script_name}...")
    runner = sys.executable
    if script_name == "make_particle_map_gif.py":
        runner = get_python_runner()
    try:
        subprocess.run([runner, str(script_path)], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing {script_name}: {e}")

def main():
    logging.info("Starting master profile generation pipeline...")
    
    pipeline_scripts = [
        "fetch_all_data.py",
        "generate_metrics.py",
        "generate_heatmap.py",
        "make_hero_svg.py",
        "make_about_svg.py",
        "make_projects_svg.py",
        "make_stack_stream_svg.py",
        "make_social_badges.py",
        "make_particle_map_gif.py"
    ]
    
    for script in pipeline_scripts:
        run_script(script)
        
    logging.info("Master profile build pipeline complete. All assets updated.")

if __name__ == "__main__":
    main()
