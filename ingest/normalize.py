from datetime import datetime


def parse_date(value):
    """Turn GitHub's date text like '2026-10-10T12:00:00Z' into a real datetime."""
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def to_document(issue, repo):
    return {
        "github_id": issue["id"],
        "repo": repo,
        "number": issue["number"],
        "title": issue["title"],
        "body": issue["body"] or "",
        "url": issue["html_url"],
        "state": issue["state"],
        "labels": [label["name"] for label in issue["labels"]],
        "author": issue["user"]["login"] if issue["user"] else None,
        "created_at": parse_date(issue["created_at"]),
        "updated_at": parse_date(issue["updated_at"]),
    }