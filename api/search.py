from ingest.db import issues
from ingest.embedding import embed_query


def build_pipeline(query_vector, limit=10, repo=None, state=None):
    vector_stage = {
        "index": "vector_index",
        "path": "embedding",
        "queryVector": query_vector,
        "numCandidates": limit * 20,  # rule of thumb: consider ~20x more than you return
        "limit": limit,
    }

    conditions = []
    if repo:
        conditions.append({"repo": repo})
    if state:
        conditions.append({"state": state})
    if len(conditions) == 1:
        vector_stage["filter"] = conditions[0]
    elif len(conditions) > 1:
        vector_stage["filter"] = {"$and": conditions}

    return [
        {"$vectorSearch": vector_stage},
        {
            "$project": {
                "_id": 0,
                "repo": 1,
                "number": 1,
                "title": 1,
                "state": 1,
                "url": 1,
                "labels": 1,
                "preview": {"$substrCP": ["$body", 0, 200]},  # first 200 characters
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]


def search_issues(query, limit=10, repo=None, state=None):
    query_vector = embed_query(query)
    return list(issues.aggregate(build_pipeline(query_vector, limit, repo, state)))