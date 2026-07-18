import requests
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
    
    # User info
    user_resp = requests.get(f"https://api.github.com/users/{username}", headers=headers)
    if user_resp.status_code != 200:
        logging.error(f"Failed to fetch user data: {user_resp.status_code}")
        return
        
    user_data = user_resp.json()
    
    # Repos info (for stars)
    repos_resp = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers)
    stars = 0
    forks = 0
    if repos_resp.status_code == 200:
        repos_data = repos_resp.json()
        for repo in repos_data:
            stars += repo.get("stargazers_count", 0)
            forks += repo.get("forks_count", 0)
            
    stats = {
        "repos": user_data.get("public_repos", 0),
        "followers": user_data.get("followers", 0),
        "following": user_data.get("following", 0),
        "stars": stars,
        "forks": forks
    }
    
    out_path = Path("data/stats.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)
        
    logging.info(f"Saved GitHub stats to {out_path}")

if __name__ == "__main__":
    fetch_github_stats()
