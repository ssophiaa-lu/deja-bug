# IssueLens Measurements

## Oct 11, 2026: After loading issues (before embeddings)

| Metric | Value |
|---|---|
| Repos | axios/axios, react/react (formerly facebook/react), TanStack/query |
| Issues stored | 3,000 (1,000 per repo) |
| Data size (uncompressed) | 6.55 MB |
| Storage size (on disk, compressed) | 2.97 MB |
| Avg. document size | 2.18 kB |
| Indexes | 2 (_id, github_id unique) |
| Total index size | 290.82 kB |
| Duplicate test | Re-ran load: 0 inserted, total stayed 3,000 |

## Oct 11, 2026: After embeddings

| Metric | Value |
|---|---|
| Embedding model | BAAI/bge-small-en-v1.5 (384 dimensions) |
| Issues embedded | 3,000 |
| Embedding time | 215.5 s (MacBook Pro, local CPU) |
| Throughput | 13.9 issues/sec |
| Re-run: skipped by content hash | 3,000 / 3,000 (100%) |
| Data size (uncompressed) | 21.62 MB |
| Storage size (on disk, compressed) | 15.73 MB |
| Avg. document size | 7.21 kB (+5.03 kB per issue for the vector) |
| Total index size | 462.85 kB |

**Observation:** compression worked well on text (storage was 45% of data size)
but poorly on vectors (storage is 73% of data size). Lists of decimals have
few repeated patterns to compress.

## Oct 11, 2026: First semantic searches

Vector Search index: `vector_index` (384 dims, cosine, filters: repo, state).
Search settings: numCandidates = 100, limit = 5.

| Query | Result quality | Notes |
|---|---|---|
| "request timeout not respected" | Good: 5/5 relevant | Matched "timeout not honored," different wording, same meaning |
| "data is undefined on first render" | Good: top 3 directly relevant | None of the top results used the phrase "first render" |
| "React app crashes when loading user data" | Weak: about 2/5 relevant | See failure reasons below |

**Failure reasons found:**
1. **Junk data:** the top result was a misfiled issue for another project (yt-dlp) posted on the React repo.
2. **Non-English issues:** a Portuguese issue ranked #4. The model is English-only.
3. **Vague queries:** broad descriptions match too many issues to rank well.

**Score observation:** good and bad results all scored between 0.859 and 0.888,
so a fixed similarity cutoff can't separate them. A threshold needs measured
data (Step 9).

## Open items
- [x] Update repo name facebook/react → react/react and re-run load (no re-embedding needed).
  One stale facebook/react issue (#24136) fell outside the new top-1,000 window and was deleted.
- [ ] Turn the three test queries above into evaluation cases in Step 9