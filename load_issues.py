from ingest.github_client import fetch_issues
from ingest.normalize import to_document
from ingest.db import ensure_indexes, upsert_issues, issues

REPOS = ["axios/axios", "facebook/react", "TanStack/query"]
ISSUES_PER_REPO = 1000

ensure_indexes()

for repo in REPOS:
    docs = [to_document(issue, repo) for issue in fetch_issues(repo, max_issues=ISSUES_PER_REPO)]
    result = upsert_issues(docs)
    print(f"{repo}: downloaded {len(docs)}, inserted {result.upserted_count}, updated {result.modified_count}")

print("Total in database:", issues.count_documents({}))