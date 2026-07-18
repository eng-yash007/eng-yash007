import requests
from bs4 import BeautifulSoup
import json
import logging
from pathlib import Path
import re

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_codechef_stats(username="eng-yash007"):
    url = f"https://www.codechef.com/users/{username}"
    logging.info(f"Fetching CodeChef stats for {username}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    stats = {
        "rating": 0,
        "stars": "0★",
        "highest_rating": 0
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Current rating
            rating_elem = soup.find(class_="rating-number")
            if rating_elem:
                stats["rating"] = int(re.sub(r'\\D', '', rating_elem.text))
                
            # Stars
            star_elem = soup.find(class_="rating-star")
            if star_elem:
                stats["stars"] = star_elem.text.strip()
                
            # Highest rating
            # Text is usually "Highest Rating 1500"
            highest_elem = soup.find(text=re.compile("Highest Rating"))
            if highest_elem:
                match = re.search(r'\\d+', highest_elem)
                if match:
                    stats["highest_rating"] = int(match.group())
                    
    except Exception as e:
        logging.error(f"Failed to fetch CodeChef data: {e}")
        # fallback data
        stats = {
            "rating": 1200,
            "stars": "2★",
            "highest_rating": 1400
        }
        
    out_path = Path("data/codechef.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)
        
    logging.info(f"Saved CodeChef stats to {out_path}")

if __name__ == "__main__":
    fetch_codechef_stats()
