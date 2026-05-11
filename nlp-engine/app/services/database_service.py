from bson import ObjectId
from app.config.database import submissions_collection
from app.utils.logging import logger

def get_previous_submissions(exclude_id: str = None):
    """Fetches stored documents from MongoDB for comparison."""
    query = {"originalText": {"$exists": True, "$ne": ""}}
    
    if exclude_id:
        try:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        except Exception:
            # If not a valid ObjectId, treat as string or skip
            query["_id"] = {"$ne": exclude_id}

    try:
        submissions = submissions_collection.find(
            query,
            {
                "_id": 1,
                "fileName": 1,
                "originalText": 1,
                "fingerprints": 1,
                "createdAt": 1
            }
        ).limit(100) # Increased limit for better coverage
        
        return list(submissions)
    except Exception as e:
        logger.error(f"Error fetching submissions from MongoDB: {str(e)}")
        return []
