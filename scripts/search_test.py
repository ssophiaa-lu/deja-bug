import sys
from ingest.db import issues
from ingest.embedding import embed_query

query = " ".join(sys.argv[1:]) or "React app crashes when loading user data"
query_vector = embed_query(query)

pipeline = [
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": query_vector,
            "numCandidates": 100,  # how many nearby vectors to consider
            "limit": 5,            # how many results to return
        }
    },
    {
        "$project": {
            "_id": 0,
            "repo": 1,
            "number": 1,
            "title": 1,
            "state": 1,
            "url": 1,
            "score": {"$meta": "vectorSearchScore"},
        }
    },
]

print(f'Query: "{query}"\n')
for r in issues.aggregate(pipeline):
    print(f"{r['score']:.3f}  [{r['repo']} #{r['number']}] ({r['state']}) {r['title']}")
    print(f"       {r['url']}")