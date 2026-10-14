"""Download only issues that changed since the last sync, then upsert them.
Run embed_issues.py afterwards to embed the ones whose text changed."""
from ingest.config import REPOS
from ingest.db import ensure_indexes, upsert_issues, get_last_synced, set_last_synced
from ingest.github_client import fetch_issues
from ingest.normalize import to_document

FIRST_SYNC_LIMIT = 1000  # a repo with no sync_state yet gets the newest 1,000 issues

ensure_indexes()

for repo in REPOS:
    last = get_last_synced(repo)
    if last is None:
        raw_issues = fetch_issues(repo, max_issues=FIRST_SYNC_LIMIT)
    else:
        # No limit: every changed issue must be seen, or the ones we skip are lost for good
        raw_issues = fetch_issues(repo, max_issues=None, since=last.strftime("%Y-%m-%dT%H:%M:%SZ"))

    docs = [to_document(issue, repo) for issue in raw_issues]
    if not docs:
        print(f"{repo}: nothing changed since {last}")
        continue

    result = upsert_issues(docs)
    # Save where we left off only after the upsert worked, so a crash means the next run retries
    set_last_synced(repo, max(d["updated_at"] for d in docs))
    print(f"{repo}: downloaded {len(docs)}, inserted {result.upserted_count}, updated {result.modified_count}")
