import urllib.request
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_leetcode_stats(username="eng-yash007"):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}"
    logging.info(f"Fetching LeetCode stats for {username}...")
    
    out_path = Path("data/leetcode.json")
    stats = {
        "totalSolved": 125,
        "easySolved": 50,
        "mediumSolved": 60,
        "hardSolved": 15,
        "ranking": 120000
    }
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                if data.get("status") == "success":
                    stats = {
                        "totalSolved": data.get("totalSolved", 125),
                        "easySolved": data.get("easySolved", 50),
                        "mediumSolved": data.get("mediumSolved", 60),
                        "hardSolved": data.get("hardSolved", 15),
                        "ranking": data.get("ranking", 120000)
                    }
    except Exception as e:
        logging.warning(f"Using cached or fallback LeetCode stats: {e}")
        
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)
        
    logging.info(f"Saved LeetCode stats to {out_path}")

if __name__ == "__main__":
    fetch_leetcode_stats()
