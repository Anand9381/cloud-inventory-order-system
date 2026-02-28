from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

db = SQLAlchemy()
mongo_client = None
mongo_db = None

import time

def init_mongo(app):
    global mongo_client, mongo_db
    uri = app.config['MONGO_URI']
    print(f"Initializing MongoDB with URI: {uri}")
    
    # Extract database name from URI
    try:
        db_name = uri.split('/')[-1].split('?')[0]
    except:
        db_name = 'inventory_logs'

    # Retry logic for MongoDB connection
    max_retries = 5
    for attempt in range(max_retries):
        try:
            mongo_client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Check connection immediately
            mongo_client.server_info()
            print("Successfully connected to MongoDB server")
            mongo_db = mongo_client[db_name]
            return
        except Exception as e:
            print(f"Attempt {attempt+1}/{max_retries} failed to connect to MongoDB: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print("Could not connect to MongoDB after multiple attempts.")
                mongo_db = None
