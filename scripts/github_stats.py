"""
GitHub Data Adapter: Fetches verified statistics and contributionsCollection using GraphQL and REST.
"""

import os
import json
import urllib.request
import logging
from bs4 import BeautifulSoup
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_github_data(username="eng-yash007"):
    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    logging.info(f"Fetching GitHub statistics for {username}...")
    
    # 1. Fetch REST user info
    user_info = {}
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            user_info = json.loads(r.read().decode())
    except Exception as e:
        logging.warning(f"Failed to fetch user REST info: {e}")

    # 2. Fetch public repos to calculate total stars
    stars_count = 0
    forks_count = 0
    repos_list = []
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}/repos?per_page=100&type=public", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            repos_data = json.loads(r.read().decode())
            for repo in repos_data:
                if not repo.get("fork", False):
                    stars_count += repo.get("stargazers_count", 0)
                    forks_count += repo.get("forks_count", 0)
                    repos_list.append({
                        "name": repo.get("name"),
                        "stars": repo.get("stargazers_count", 0),
                        "language": repo.get("language")
                    })
    except Exception as e:
        logging.warning(f"Failed to fetch repos for stars: {e}")

    # 3. Fetch contributionsCollection via GraphQL if token available
    contributions_data = None
    if token:
        graphql_query = """
        query($login: String!) {
          user(login: $login) {
            contributionsCollection {
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    date
                    contributionCount
                    contributionLevel
                    weekday
                  }
                }
                months {
                  name
                  year
                  firstDay
                  totalWeeks
                }
              }
            }
          }
        }
        """
        try:
            req_data = json.dumps({"query": graphql_query, "variables": {"login": username}}).encode("utf-8")
            req = urllib.request.Request("https://api.github.com/graphql", data=req_data, headers={
                **headers, "Content-Type": "application/json"
            })
            with urllib.request.urlopen(req, timeout=12) as r:
                res = json.loads(r.read().decode())
                cal = res.get("data", {}).get("user", {}).get("contributionsCollection", {}).get("contributionCalendar")
                if cal:
                    contributions_data = cal
                    logging.info(f"Retrieved GraphQL contributions: {cal.get('totalContributions')} total")
        except Exception as e:
            logging.warning(f"GraphQL contributions retrieval failed: {e}")

    # 4. Fallback to public contributions page scraping if GraphQL unavailable
    if not contributions_data:
        logging.info("Falling back to public contribution calendar scraping...")
        try:
            req = urllib.request.Request(f"https://github.com/users/{username}/contributions", headers=headers)
            with urllib.request.urlopen(req, timeout=10) as r:
                html = r.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                
                # Extract total count from heading
                h2 = soup.find("h2")
                total_contribs = 0
                if h2:
                    nums = [int(s) for s in h2.text.split() if s.isdigit()]
                    if nums:
                        total_contribs = nums[0]

                # Extract days
                days = []
                for td in soup.find_all("td", class_="ContributionCalendar-day"):
                    date = td.get("data-date")
                    if not date:
                        continue
                    level_str = td.get("data-level", "0")
                    level = int(level_str) if level_str.isdigit() else 0
                    
                    tid = td.get("id")
                    count = 0
                    if tid:
                        tt = soup.find("tool-tip", attrs={"for": tid})
                        if tt and not tt.text.strip().lower().startswith("no"):
                            parts = tt.text.strip().split()
                            if parts and parts[0].isdigit():
                                count = int(parts[0])
                            else:
                                count = level * 2 if level > 0 else 0
                    days.append({
                        "date": date,
                        "contributionCount": count,
                        "contributionLevel": level
                    })

                # Reconstruct weeks (7 days per week)
                weeks = []
                for i in range(0, len(days), 7):
                    chunk = days[i:i+7]
                    for w_idx, day_obj in enumerate(chunk):
                        day_obj["weekday"] = w_idx
                    weeks.append({"contributionDays": chunk})

                contributions_data = {
                    "totalContributions": total_contribs if total_contribs > 0 else sum(d["contributionCount"] for d in days),
                    "weeks": weeks
                }
                logging.info(f"Scraped {len(days)} days, total contributions: {contributions_data['totalContributions']}")
        except Exception as e:
            logging.error(f"Failed to scrape contributions page: {e}")

    return {
        "status": "success" if user_info else "error",
        "username": username,
        "public_repos": user_info.get("public_repos", len(repos_list) if repos_list else "Unavailable"),
        "followers": user_info.get("followers", "Unavailable"),
        "following": user_info.get("following", "Unavailable"),
        "total_stars": stars_count,
        "total_forks": forks_count,
        "contributions": contributions_data
    }

if __name__ == "__main__":
    res = fetch_github_data()
    print("GitHub Result Summary:", {k: v for k, v in res.items() if k != "contributions"})
