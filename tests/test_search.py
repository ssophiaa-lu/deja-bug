from api.search import build_pipeline

# build_pipeline only builds a list of dicts, so any short vector works: no model, no Atlas
FAKE_VECTOR = [0.1, 0.2, 0.3]


def vector_stage(pipeline):
    return pipeline[0]["$vectorSearch"]


def test_no_filters_means_no_filter_key():
    stage = vector_stage(build_pipeline(FAKE_VECTOR, limit=5))
    assert "filter" not in stage
    assert stage["limit"] == 5
    assert stage["numCandidates"] == 100


def test_single_filter_is_used_directly():
    stage = vector_stage(build_pipeline(FAKE_VECTOR, repo="axios/axios"))
    assert stage["filter"] == {"repo": "axios/axios"}


def test_two_filters_are_combined_with_and():
    stage = vector_stage(build_pipeline(FAKE_VECTOR, repo="axios/axios", state="open"))
    assert stage["filter"] == {"$and": [{"repo": "axios/axios"}, {"state": "open"}]}
