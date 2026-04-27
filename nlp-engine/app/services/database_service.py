from app.config.database import submissions_collection


def get_previous_submissions():
    submissions = submissions_collection.find(
        {
            "originalText": {"$exists": True, "$ne": ""}
        },
        {
            "fileName": 1,
            "originalText": 1,
            "fingerprints": 1,
            "createdAt": 1
        }
    ).limit(50)

    return list(submissions)
