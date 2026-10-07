import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["job_portal"]

jobs_collection = db["jobs"]
users_collection = db["users"]
applications_collection = db["applications"]

print("MongoDB connection established")