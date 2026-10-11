import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
    "Accept": "application/vnd.github+json",
}


def fetch_issues(repo, max_issues=1000, since=None):
    """Yield issues (not pull requests) from a repo, most recently updated first."""
    url = f"{API_URL}/repos/{repo}/issues"
    params = {
        "state": "all",        # open AND closed issues
        "per_page": 100,       # the maximum GitHub allows per page
        "sort": "updated",
        "direction": "desc",
    }
    if since:
        params["since"] = since  # only issues updated after this time (used in Step 6)

    count = 0
    while url and count < max_issues:
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        response.raise_for_status()  # stop with an error if GitHub says something went wrong

        for item in response.json():
            if "pull_request" in item:  # this endpoint mixes in PRs; skip them
                continue
            yield item
            count += 1
            if count >= max_issues:
                return

        # GitHub tells us where the next page is in the response headers
        url = response.links.get("next", {}).get("url")
        params = None  # the "next" URL already contains all the parameters