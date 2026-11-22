import urllib.request
import json
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_github_stats(username="eng-yash007"):
    headers = {"User-Agent": "Mozilla/5.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    logging.info(f"Fetching GitHub stats for {username}...")
    
    out_path = Path("data/stats.json")
    
    # User info
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                user_data = json.loads(resp.read().decode())
            else:
                user_data = {}
    except Exception as e:
        logging.warning(f"Could not fetch user info: {e}")
        user_data = {}

    stars = 3
    forks = 0
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                repos_data = json.loads(resp.read().decode())
                stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
                forks = sum(repo.get("forks_count", 0) for repo in repos_data)
    except Exception as e:
        logging.warning(f"Could not fetch repos info: {e}")

    stats = {
        "repos": user_data.get("public_repos", 10),
        "followers": user_data.get("followers", 1),
        "following": user_data.get("following", 0),
        "stars": stars,
        "forks": forks
    }
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)
        
    logging.info(f"Saved GitHub stats to {out_path}")

if __name__ == "__main__":
    fetch_github_stats()
