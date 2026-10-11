import hashlib
from fastembed import TextEmbedding

MODEL_NAME = "BAAI/bge-small-en-v1.5"
MAX_BODY_CHARS = 2000  # the model only reads roughly the first 512 tokens anyway

_model = None


def get_model():
    """Load the model once and reuse it (loading is slow)."""
    global _model
    if _model is None:
        _model = TextEmbedding(MODEL_NAME)
    return _model


def issue_text(title, body):
    """The exact text we turn into a vector for an issue."""
    return f"{title}\n\n{(body or '')[:MAX_BODY_CHARS]}"


def content_hash(text):
    """A short fingerprint of the text. Same text always gives the same hash."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def embed_issues(texts):
    """Vectors for stored issues (documents)."""
    return [v.tolist() for v in get_model().passage_embed(texts)]


def embed_query(text):
    """Vector for a user's search query. Used in Step 4."""
    return next(get_model().query_embed(text)).tolist()