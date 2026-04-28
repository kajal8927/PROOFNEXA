from pymongo import MongoClient
from app.config.config import settings

# Initialize MongoDB Client
client = MongoClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]
submissions_collection = db[settings.COLLECTION_NAME]

def get_db_status():
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        return True
    except Exception:
        return False
