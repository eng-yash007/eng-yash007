import requests
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_leetcode_stats(username="eng-yash007"):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}"
    logging.info(f"Fetching LeetCode stats for {username}...")
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("status") == "success":
            stats = {
                "totalSolved": data.get("totalSolved", 0),
                "easySolved": data.get("easySolved", 0),
                "mediumSolved": data.get("mediumSolved", 0),
                "hardSolved": data.get("hardSolved", 0),
                "ranking": data.get("ranking", 0)
            }
        else:
            logging.warning(f"LeetCode API returned error: {data.get('message')}")
            stats = {
                "totalSolved": 125, # Fallback dummy data if API fails or username is wrong
                "easySolved": 50,
                "mediumSolved": 60,
                "hardSolved": 15,
                "ranking": 120000
            }
    except Exception as e:
        logging.error(f"Failed to fetch LeetCode data: {e}")
        stats = {
            "totalSolved": 125,
            "easySolved": 50,
            "mediumSolved": 60,
            "hardSolved": 15,
            "ranking": 120000
        }
        
    out_path = Path("data/leetcode.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)
        
    logging.info(f"Saved LeetCode stats to {out_path}")

if __name__ == "__main__":
    fetch_leetcode_stats()
