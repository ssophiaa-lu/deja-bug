# IssueLens Measurements

## Oct 11, 2026: After loading issues (before embeddings)

| Metric | Value |
|---|---|
| Repos | axios/axios, facebook/react, TanStack/query |
| Issues stored | 3,000 (1,000 per repo) |
| Data size (uncompressed) | 6.55 MB |
| Storage size (on disk, compressed) | 2.97 MB |
| Avg. document size | 2.18 kB |
| Indexes | 2 (_id, github_id unique) |
| Total index size | 290.82 kB |
| Duplicate test | Re-ran load: 0 inserted, total stayed 3,000 |

## After embeddings

| Metric | Value |
|---|---|
| Embedding model | BAAI/bge-small-en-v1.5 (384 dimensions) |
| Issues embedded | |
| Embedding time | |
| Throughput (issues/sec) | |
| Re-run: skipped by content hash | |
| Data size | |
| Storage size | |