import certifi
from pymongo import MongoClient
from src.config import MONGODB_URI, DB_NAME, MANUAL_COLLECTION, PRODUCTS_COLLECTION

_client = None
_db = None
manual_collection = None
products_collection = None

if MONGODB_URI:
    _client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
    _db = _client[DB_NAME]
    manual_collection = _db[MANUAL_COLLECTION]
    products_collection = _db[PRODUCTS_COLLECTION]
    
    # Optional: verify connection
    try:
        _client.admin.command("ping")
    except Exception as e:
        print(f"Warning: MongoDB connection failed: {e}")
