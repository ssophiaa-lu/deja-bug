import time
from pymongo import UpdateOne
from ingest.db import issues
from ingest.embedding import MODEL_NAME, issue_text, content_hash, embed_issues

BATCH_SIZE = 64

# 1. Decide which issues actually need a new embedding
to_embed = []
skipped = 0
for doc in issues.find({}, {"title": 1, "body": 1, "content_hash": 1, "embedding_model": 1}):
    text = issue_text(doc["title"], doc["body"])
    new_hash = content_hash(text)
    if doc.get("content_hash") == new_hash and doc.get("embedding_model") == MODEL_NAME:
        skipped += 1
        continue
    to_embed.append((doc["_id"], text, new_hash))

print(f"Need embeddings: {len(to_embed)}, skipped (unchanged): {skipped}")

# 2. Embed in batches and save
start_time = time.perf_counter()
for start in range(0, len(to_embed), BATCH_SIZE):
    batch = to_embed[start:start + BATCH_SIZE]
    vectors = embed_issues([text for _, text, _ in batch])
    operations = [
        UpdateOne(
            {"_id": doc_id},
            {"$set": {"embedding": vector, "content_hash": h, "embedding_model": MODEL_NAME}},
        )
        for (doc_id, _, h), vector in zip(batch, vectors)
    ]
    issues.bulk_write(operations)
    print(f"Embedded {start + len(batch)}/{len(to_embed)}")

elapsed = time.perf_counter() - start_time
if to_embed:
    print(f"Done in {elapsed:.1f}s ({len(to_embed) / elapsed:.1f} issues/sec)")