import os
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, UpdateOne

load_dotenv()

client = MongoClient(os.environ["MONGODB_URI"])
db = client["issuelens"]
issues = db["issues"]


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