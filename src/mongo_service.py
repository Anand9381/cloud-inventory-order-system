from datetime import datetime
import src.extensions as extensions

def log_activity(uid, action, details):
    """
    Logs user activity to MongoDB.
    """
    try:
        if extensions.mongo_db is not None:
            log_entry = {
                'user_id': uid,
                'action': action,
                'details': details,
                'timestamp': datetime.utcnow()
            }
            # Attempt insert
            result = extensions.mongo_db.logs.insert_one(log_entry)
            print(f"Logged to MongoDB: {action} by User {uid}. Inserted ID: {result.inserted_id}")
        else:
            print("MongoDB not initialized (extensions.mongo_db is None), skipping log.")
    except Exception as e:
        print(f"FAILED to log to MongoDB: {e}")

def get_logs(limit=50, start_date=None, end_date=None):
    """
    Retrieves recent logs from MongoDB with optional date filtering.
    """
    if extensions.mongo_db is not None:
        query = {}
        if start_date or end_date:
            query['timestamp'] = {}
            if start_date:
                try:
                    if isinstance(start_date, str):
                        start_date = datetime.fromisoformat(start_date)
                    query['timestamp']['$gte'] = start_date
                except ValueError:
                    pass # Invalid date format, ignore
            if end_date:
                try:
                    if isinstance(end_date, str):
                        end_date = datetime.fromisoformat(end_date)
                    query['timestamp']['$lte'] = end_date
                except ValueError:
                    pass

        logs = list(extensions.mongo_db.logs.find(query).sort('timestamp', -1).limit(limit))
        for log in logs:
            log['_id'] = str(log['_id']) # Convert ObjectId to string
        return logs
    return []

def get_log_count():
    """Returns the total number of log entries in MongoDB"""
    if extensions.mongo_db is not None:
        return extensions.mongo_db.logs.count_documents({})
    return 0
    return []
