import requests
from bs4 import BeautifulSoup
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_contributions(username="eng-yash007"):
    url = f"https://github.com/users/{username}/contributions"
    logging.info(f"Fetching contributions from {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logging.error(f"Failed to fetch data: {response.status_code}")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Github heatmap rows
    # The new layout has tbody with trs for each day of the week (0-6)
    # inside which there are tds for each week (0-52)
    weeks = soup.select('tbody > tr > td.ContributionCalendar-day')
    
    contributions = []
    total_contributions = 0
    current_streak = 0
    longest_streak = 0
    best_day_count = 0
    best_day_date = ""
    
    # We might not get exact counts from HTML easily anymore without tooltips,
    # but we can get the level (0-4) and parse the text content if available.
    for day in weeks:
        date = day.get('data-date')
        if not date:
            continue
            
        level = int(day.get('data-level', 0))
        
        # Try to extract exact count from the tooltip or ID
        # "No contributions on Sunday, Jan 1, 2023" or "5 contributions on..."
        tooltip_id = day.get('id')
        count = 0
        if tooltip_id:
            tooltip = soup.select_one(f'tool-tip[for="{tooltip_id}"]')
            if tooltip:
                text = tooltip.text.strip()
                if text.lower().startswith('no '):
                    count = 0
                else:
                    try:
                        count = int(text.split(' ')[0])
                    except:
                        count = level * 3 # rough fallback
                        
        total_contributions += count
        
        if count > best_day_count:
            best_day_count = count
            best_day_date = date
            
        if count > 0:
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak
        else:
            current_streak = 0
            
        contributions.append({
            "date": date,
            "level": level,
            "count": count
        })

    # The streak calculation needs to go backwards from today to be accurate for "current"
    # But since this is a simple script, we just calculate from the fetched array.
    
    # Re-calculate correct current streak by walking backward
    current_streak = 0
    for day in reversed(contributions):
        # Stop at today (sometimes future days are in the graph as level 0)
        day_date = datetime.strptime(day["date"], "%Y-%m-%d").date()
        if day_date > datetime.now().date():
            continue
        if day["count"] > 0:
            current_streak += 1
        else:
            if current_streak > 0:
                break
                
    data = {
        "total": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day_count": best_day_count,
        "best_day_date": best_day_date,
        "days": contributions
    }
    
    out_path = Path("data/contributions.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    logging.info(f"Saved contributions to {out_path}")

if __name__ == "__main__":
    fetch_contributions()
