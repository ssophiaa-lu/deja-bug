import pytest
import requests

import ingest.github_client as github_client


def fake_response(status_code):
    response = requests.Response()
    response.status_code = status_code
    return response


@pytest.fixture
def fake_github(monkeypatch):
    """Replace requests.get with a script of outcomes, and time.sleep with a recorder (no real waiting)."""
    outcomes = []  # each test fills this: a status code to return, or an exception to raise
    calls = []
    waits = []

    def fake_get(url, **kwargs):
        calls.append(url)
        outcome = outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return fake_response(outcome)

    monkeypatch.setattr(github_client.requests, "get", fake_get)
    monkeypatch.setattr(github_client.time, "sleep", waits.append)
    return outcomes, calls, waits


def test_retries_a_502_then_succeeds(fake_github):
    outcomes, calls, waits = fake_github
    outcomes.extend([502, 200])
    response = github_client.get_with_retries("https://api.github.com/x", None)
    assert response.status_code == 200
    assert len(calls) == 2


def test_gives_up_after_max_attempts(fake_github):
    outcomes, calls, waits = fake_github
    outcomes.extend([502] * github_client.MAX_ATTEMPTS)
    with pytest.raises(requests.HTTPError):
        github_client.get_with_retries("https://api.github.com/x", None)
    assert len(calls) == github_client.MAX_ATTEMPTS


def test_404_fails_without_retrying(fake_github):
    outcomes, calls, waits = fake_github
    outcomes.append(404)
    with pytest.raises(requests.HTTPError):
        github_client.get_with_retries("https://api.github.com/x", None)
    assert len(calls) == 1
    assert waits == []


def test_retries_a_network_error_then_succeeds(fake_github):
    outcomes, calls, waits = fake_github
    outcomes.extend([requests.ConnectionError("wifi dropped"), 200])
    response = github_client.get_with_retries("https://api.github.com/x", None)
    assert response.status_code == 200
    assert len(calls) == 2
