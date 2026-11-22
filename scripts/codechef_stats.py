"""
CodeChef Data Adapter: Fetches verified public statistics from CodeChef public profile.
Never fabricates ratings; supports caching and graceful failure handling.
"""

import urllib.request
import re
import json
import logging
from bs4 import BeautifulSoup
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

CACHE_FILE = Path("data/codechef_cache.json")

def fetch_codechef_data(username="yashgupta9171"):
    logging.info(f"Fetching CodeChef statistics for {username}...")
    url = f"https://www.codechef.com/users/{username}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as response:
            if response.status == 200:
                html = response.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                
                # Rating number
                rating_elem = soup.find("div", class_="rating-number")
                rating_val = "Unavailable"
                if rating_elem:
                    nums = re.findall(r"\d+", rating_elem.text.strip())
                    if nums:
                        rating_val = int(nums[0])
                        
                # Stars
                star_elem = soup.find("span", class_="rating")
                stars_val = "Unavailable"
                if star_elem:
                    stars_val = star_elem.text.strip()
                elif rating_val != "Unavailable":
                    # Derive stars from rating threshold if badge text omitted
                    r = int(rating_val)
                    if r < 1400: stars_val = "1★"
                    elif r < 1600: stars_val = "2★"
                    elif r < 1800: stars_val = "3★"
                    elif r < 2000: stars_val = "4★"
                    elif r < 2200: stars_val = "5★"
                    elif r < 2500: stars_val = "6★"
                    else: stars_val = "7★"
                    
                # Ranks
                global_rank = "Unavailable"
                country_rank = "Unavailable"
                ranks_div = soup.find("div", class_="rating-ranks")
                if ranks_div:
                    m_g = re.search(r"Global Rank\s*(\d+)", ranks_div.text)
                    if m_g:
                        global_rank = int(m_g.group(1))
                    m_c = re.search(r"Country Rank\s*(\d+)", ranks_div.text)
                    if m_c:
                        country_rank = int(m_c.group(1))
                        
                # Highest rating
                highest_rating = "Unavailable"
                for small in soup.find_all("small"):
                    if "Highest Rating" in small.text:
                        m_h = re.search(r"Highest Rating\s*(\d+)", small.text)
                        if m_h:
                            highest_rating = int(m_h.group(1))
                            
                stats = {
                    "status": "success",
                    "username": username,
                    "rating": rating_val,
                    "stars": stars_val,
                    "highest_rating": highest_rating,
                    "global_rank": global_rank,
                    "country_rank": country_rank,
                    "is_cached": False
                }
                
                CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(CACHE_FILE, "w", encoding="utf-8") as f:
                    json.dump(stats, f, indent=2)
                    
                logging.info(f"Successfully retrieved CodeChef stats: Rating={rating_val}, Stars={stars_val}, Rank={global_rank}")
                return stats
    except Exception as e:
        logging.warning(f"Live CodeChef fetch failed: {e}")

    # Fallback to cache if available
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cached = json.load(f)
                cached["is_cached"] = True
                logging.info("Returning cached CodeChef statistics.")
                return cached
        except Exception:
            pass

    return {
        "status": "unavailable",
        "username": username,
        "rating": "Unavailable",
        "stars": "Unavailable",
        "highest_rating": "Unavailable",
        "global_rank": "Unavailable",
        "country_rank": "Unavailable",
        "is_cached": False
    }

if __name__ == "__main__":
    data = fetch_codechef_data()
    print(json.dumps(data, indent=2))
