import subprocess
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def run_script(script_name: str):
    script_path = Path("scripts") / script_name
    if not script_path.exists():
        logging.warning(f"Script {script_path} not found. Skipping.")
        return
    logging.info(f"Running {script_name}...")
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run {script_name}: {e}")

def main():
    logging.info("Starting build process...")
    
    # Scripts to run in order
    scripts = [
        "prep_photo.py",
        "make_ascii_svg.py",
        "fetch_contributions.py",
        "render_heatmap.py",
        "make_info_card.py",
        "make_skills_svg.py",
        "make_timeline_svg.py"
    ]
    
    for script in scripts:
        run_script(script)
        
    logging.info("Build complete.")

if __name__ == "__main__":
    main()
