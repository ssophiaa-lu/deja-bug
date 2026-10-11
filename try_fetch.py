from ingest.github_client import fetch_issues

issues = list(fetch_issues("axios/axios", max_issues=150))
print("Downloaded:", len(issues))

first = issues[0]
print(first["number"], first["title"])
print(list(first.keys()))