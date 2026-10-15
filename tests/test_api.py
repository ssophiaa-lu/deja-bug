from fastapi.testclient import TestClient
from pymongo.errors import PyMongoError

import api.main as main

# Not used with "with", so startup (loading the model) doesn't run: tests stay fast
client = TestClient(main.app)

FAKE_RESULT = {
    "repo": "axios/axios",
    "number": 5886,
    "title": "axios timeout not respected for chunked requests",
    "state": "closed",
    "url": "https://github.com/axios/axios/issues/5886",
    "labels": ["bug"],
    "preview": "When using chunked requests...",
    "score": 0.875,
}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_repos_lists_known_repos():
    response = client.get("/repos")
    assert response.status_code == 200
    assert "axios/axios" in response.json()["repos"]


def test_search_returns_results(monkeypatch):
    monkeypatch.setattr(main, "search_issues", lambda *args: [FAKE_RESULT])
    response = client.post("/search", json={"query": "timeout not respected"})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert body["results"][0]["number"] == 5886


def test_filters_are_passed_to_search(monkeypatch):
    received = {}

    def fake_search(query, limit, repo, state):
        received.update(query=query, limit=limit, repo=repo, state=state)
        return []

    monkeypatch.setattr(main, "search_issues", fake_search)
    client.post("/search", json={"query": "timeout", "repo": "axios/axios", "state": "open", "limit": 3})
    assert received == {"query": "timeout", "limit": 3, "repo": "axios/axios", "state": "open"}


def test_query_too_short_is_rejected():
    assert client.post("/search", json={"query": "hi"}).status_code == 422


def test_unknown_repo_is_rejected():
    assert client.post("/search", json={"query": "timeout", "repo": "string"}).status_code == 422


def test_invalid_state_is_rejected():
    assert client.post("/search", json={"query": "timeout", "state": "maybe"}).status_code == 422


def test_limit_too_large_is_rejected():
    assert client.post("/search", json={"query": "timeout", "limit": 500}).status_code == 422


def test_frontend_origin_is_allowed():
    response = client.get("/health", headers={"Origin": "http://localhost:5173"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_other_origin_is_not_allowed():
    response = client.get("/health", headers={"Origin": "https://some-other-site.com"})
    assert "access-control-allow-origin" not in response.headers


def test_database_error_returns_503(monkeypatch):
    def broken_search(*args):
        raise PyMongoError("connection lost")

    monkeypatch.setattr(main, "search_issues", broken_search)
    response = client.post("/search", json={"query": "timeout"})
    assert response.status_code == 503