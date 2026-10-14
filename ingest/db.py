import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, UpdateOne

load_dotenv()

client = MongoClient(os.environ["MONGODB_URI"])
db = client["issuelens"]
issues = db["issues"]
sync_state = db["sync_state"]  # one document per repo: where the last sync left off


def ensure_indexes():
    """Make github_id unique so the same issue can never be stored twice."""
    issues.create_index([("github_id", ASCENDING)], unique=True)


def upsert_issues(docs):
    """Insert new issues and update existing ones, in one round trip."""
    if not docs:
        return None
    operations = [
        UpdateOne({"github_id": d["github_id"]}, {"$set": d}, upsert=True)
        for d in docs
    ]
    return issues.bulk_write(operations)


def get_last_synced(repo):
    """The newest updated_at we've already stored for this repo, or None if never synced."""
    state = sync_state.find_one({"_id": repo})
    return state["last_updated_at"] if state else None


def set_last_synced(repo, last_updated_at):
    """Remember the newest updated_at we saw, so the next sync starts from there."""
    sync_state.update_one(
        {"_id": repo},
        {"$set": {"last_updated_at": last_updated_at, "synced_at": datetime.now(timezone.utc)}},
        upsert=True,
    )