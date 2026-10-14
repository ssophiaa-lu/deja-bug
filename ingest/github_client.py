import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
    "Accept": "application/vnd.github+json",
}
MAX_ATTEMPTS = 4
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}  # temporary: trying again may work


def get_with_retries(url, params):
    """GET a GitHub URL, retrying temporary failures after waiting 1s, 2s, then 4s."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        except (requests.ConnectionError, requests.Timeout):
            if attempt == MAX_ATTEMPTS:
                raise  # out of tries: let the error stop the sync
        else:  # runs only if requests.get didn't raise
            if response.status_code not in RETRY_STATUS_CODES or attempt == MAX_ATTEMPTS:
                response.raise_for_status()  # 401, 404, ... fail right away: retrying won't help
                return response
        time.sleep(2 ** (attempt - 1))  # 1s, 2s, 4s


def fetch_issues(repo, max_issues=1000, since=None):
    """Yield issues (not pull requests) from a repo, most recently updated first.
    max_issues=None means no limit."""
    url = f"{API_URL}/repos/{repo}/issues"
    params = {
        "state": "all",        # open AND closed issues
        "per_page": 100,       # the maximum GitHub allows per page
        "sort": "updated",
        "direction": "desc",
    }
    if since:
        params["since"] = since  # only issues updated at or after this time

    count = 0
    while url and (max_issues is None or count < max_issues):
        response = get_with_retries(url, params)

        for item in response.json():
            if "pull_request" in item:  # this endpoint mixes in PRs; skip them
                continue
            yield item
            count += 1
            if max_issues is not None and count >= max_issues:
                return

        # GitHub tells us where the next page is in the response headers
        url = response.links.get("next", {}).get("url")
        params = None  # the "next" URL already contains all the parameters