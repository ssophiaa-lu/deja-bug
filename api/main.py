from contextlib import asynccontextmanager
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from pymongo.errors import PyMongoError

from api.search import search_issues
from ingest.config import REPOS
from ingest.embedding import get_model


@asynccontextmanager
async def lifespan(app):
    get_model()  # load the embedding model once at startup, not on the first search
    yield


app = FastAPI(title="IssueLens API", lifespan=lifespan)


class SearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=2000)
    repo: Optional[str] = None
    state: Optional[Literal["open", "closed"]] = None
    limit: int = Field(default=10, ge=1, le=50)

    @field_validator("repo")
    @classmethod
    def repo_must_be_known(cls, value):
        if value is not None and value not in REPOS:
            raise ValueError(f"Unknown repo. Choose one of: {', '.join(REPOS)}")
        return value


class SearchResult(BaseModel):
    repo: str
    number: int
    title: str
    state: str
    url: str
    labels: list[str]
    preview: str
    score: float


class SearchResponse(BaseModel):
    query: str
    count: int
    results: list[SearchResult]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/repos")
def repos():
    """The repos users can filter by. The website will use this for its dropdown."""
    return {"repos": REPOS}


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    try:
        results = search_issues(request.query, request.limit, request.repo, request.state)
    except PyMongoError:
        raise HTTPException(status_code=503, detail="Search is temporarily unavailable. Please try again.")
    return SearchResponse(query=request.query, count=len(results), results=results)