#!/usr/bin/env python3
"""
Dynamic GitHub Profile Terminal Updater (Zero External Dependencies).
Fetches live GitHub profile telemetry (public repos, stars, followers)
for @dedyirama-id.
"""

import json
import os
import urllib.request
from datetime import datetime, timezone

GITHUB_USERNAME = os.environ.get("GITHUB_ACTOR", "dedyirama-id")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def fetch_github_stats(username: str) -> dict:
    headers = {
        "User-Agent": "Cyberdeck-Terminal-Updater",
        "Accept": "application/vnd.github+json",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    user_url = f"https://api.github.com/users/{username}"
    req = urllib.request.Request(user_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        user_data = json.loads(resp.read().decode("utf-8"))

    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&type=owner"
    req_repos = urllib.request.Request(repos_url, headers=headers)
    with urllib.request.urlopen(req_repos, timeout=10) as resp:
        repos_data = json.loads(resp.read().decode("utf-8"))

    total_stars = sum(r.get("stargazers_count", 0) for r in repos_data)
    public_repos = user_data.get("public_repos", len(repos_data))
    followers = user_data.get("followers", 0)

    return {
        "username": username,
        "public_repos": public_repos,
        "total_stars": total_stars,
        "followers": followers,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }


if __name__ == "__main__":
    try:
        stats = fetch_github_stats(GITHUB_USERNAME)
        print(f"[OK] Fetched telemetry for @{stats['username']}: {stats}")
    except Exception as exc:
        print(f"[WARN] Could not fetch live GitHub API stats: {exc}")
