"""
LeetCode Data Adapter: Fetches verified public statistics from LeetCode GraphQL endpoint.
Never fabricates stats; supports caching and graceful failure handling.
"""

import urllib.request
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

CACHE_FILE = Path("data/leetcode_cache.json")

def fetch_leetcode_data(username="eng-yash007"):
    logging.info(f"Fetching LeetCode statistics for {username}...")
    
    url = "https://leetcode.com/graphql"
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
        profile {
          ranking
          reputation
        }
      }
      userContestRanking(username: $username) {
        rating
        globalRanking
        attendedContestsCount
      }
    }
    """
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Referer": f"https://leetcode.com/{username}/"
    }
    
    try:
        req_data = json.dumps({"query": query, "variables": {"username": username}}).encode("utf-8")
        req = urllib.request.Request(url, data=req_data, headers=headers)
        
        with urllib.request.urlopen(req, timeout=12) as response:
            if response.status == 200:
                result = json.loads(response.read().decode())
                matched = result.get("data", {}).get("matchedUser")
                if matched:
                    subs = matched.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
                    total_solved = "Unavailable"
                    easy_solved = "Unavailable"
                    med_solved = "Unavailable"
                    hard_solved = "Unavailable"
                    
                    for sub in subs:
                        diff = sub.get("difficulty")
                        cnt = sub.get("count")
                        if diff == "All":
                            total_solved = cnt
                        elif diff == "Easy":
                            easy_solved = cnt
                        elif diff == "Medium":
                            med_solved = cnt
                        elif diff == "Hard":
                            hard_solved = cnt
                            
                    ranking = matched.get("profile", {}).get("ranking", "Unavailable")
                    contest = result.get("data", {}).get("userContestRanking") or {}
                    contest_rating = contest.get("rating", "Unavailable")
                    
                    stats = {
                        "status": "success",
                        "username": username,
                        "total_solved": total_solved,
                        "easy_solved": easy_solved,
                        "medium_solved": med_solved,
                        "hard_solved": hard_solved,
                        "ranking": ranking,
                        "contest_rating": contest_rating if contest_rating != "Unavailable" else None,
                        "is_cached": False
                    }
                    
                    # Update cache
                    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
                    with open(CACHE_FILE, "w", encoding="utf-8") as f:
                        json.dump(stats, f, indent=2)
                        
                    logging.info(f"Successfully retrieved real LeetCode stats: Total={total_solved}, Ranking={ranking}")
                    return stats
    except Exception as e:
        logging.warning(f"Live LeetCode fetch failed: {e}")

    # Fallback to cache if available
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cached = json.load(f)
                cached["is_cached"] = True
                logging.info("Returning cached LeetCode statistics.")
                return cached
        except Exception:
            pass

    return {
        "status": "unavailable",
        "username": username,
        "total_solved": "Unavailable",
        "easy_solved": "Unavailable",
        "medium_solved": "Unavailable",
        "hard_solved": "Unavailable",
        "ranking": "Unavailable",
        "contest_rating": None,
        "is_cached": False
    }

if __name__ == "__main__":
    data = fetch_leetcode_data()
    print(json.dumps(data, indent=2))

