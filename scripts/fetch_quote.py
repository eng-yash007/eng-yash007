import requests
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_daily_quote():
    url = "https://zenquotes.io/api/random"
    logging.info("Fetching random programming quote...")
    
    quote_data = {
        "quote": "Programs must be written for people to read, and only incidentally for machines to execute.",
        "author": "Harold Abelson"
    }
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                quote_data["quote"] = data[0].get("q", quote_data["quote"])
                quote_data["author"] = data[0].get("a", quote_data["author"])
    except Exception as e:
        logging.error(f"Failed to fetch quote: {e}")
        
    out_path = Path("data/quotes.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(quote_data, f, indent=4)
        
    logging.info(f"Saved quote to {out_path}")

if __name__ == "__main__":
    fetch_daily_quote()
