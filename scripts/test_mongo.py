import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
print(MongoClient(os.environ["MONGODB_URI"]).admin.command("ping"))

