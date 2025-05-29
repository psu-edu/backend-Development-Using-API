import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["weather_db"]
collection = db["weather_data"]

def save_to_mongo(data):
    collection.insert_one(data)
    print("📥 Saved to MongoDB.")
