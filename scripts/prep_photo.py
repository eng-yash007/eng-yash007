import cv2
import numpy as np
from rembg import remove
from PIL import Image, ImageEnhance
import io
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def process_photo(input_path: str, output_path: str):
    input_file = Path(input_path)
    if not input_file.exists():
        logging.error(f"Input file {input_path} not found.")
        return False
        
    logging.info(f"Removing background from {input_path}...")
    with open(input_path, "rb") as f:
        input_data = f.read()
    
    # Remove background
    try:
        subject_data = remove(input_data)
        subject_img = Image.open(io.BytesIO(subject_data)).convert("RGBA")
    except Exception as e:
        logging.error(f"Error removing background: {e}")
        return False

    # Create a black background (as terminal is dark)
    background = Image.new("RGBA", subject_img.size, (0, 0, 0, 255))
    combined = Image.alpha_composite(background, subject_img)
    
    # Convert to grayscale
    gray_img = combined.convert("L")
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(gray_img)
    enhanced_img = enhancer.enhance(1.5)
    
    # Apply CLAHE using OpenCV
    img_array = np.array(enhanced_img)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(img_array)
    
    # Save processed image
    final_img = Image.fromarray(cl1)
    # Resize slightly for better ASCII aspect ratio if needed (optional)
    
    final_img.save(output_path)
    logging.info(f"Saved processed photo to {output_path}")
    return True

if __name__ == "__main__":
    # Check for yash_image.png or profile-photo.png
    input_options = ["data/yash_image.png", "data/profile-photo.png"]
    processed = False
    
    for opt in input_options:
        if Path(opt).exists():
            processed = process_photo(opt, "data/processed_photo.png")
            if processed:
                break
                
    if not processed:
        logging.warning("No input photo found. Place yash_image.png in data/ directory.")
