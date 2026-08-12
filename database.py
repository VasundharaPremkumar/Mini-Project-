import os
from motor.motor_asyncio import AsyncIOMotorClient

# Using local MongoDB since the user is installing it on their PC
MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.crime_network

# Collections
users_collection = database.get_collection("users")
crimes_collection = database.get_collection("crimes")
ncrb_collection = database.get_collection("ncrb_states")

# Helper to format MongoDB outputs to dict
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"],
    }

def crime_helper(crime) -> dict:
    return {
        "id": str(crime["_id"]),
        "date": crime.get("date"),
        "time": crime.get("time"),
        "location": crime.get("location"),
        "crime_type": crime.get("crime_type"),
        "weapon": crime.get("weapon"),
        "suspect_profile": crime.get("suspect_profile"),
        "description": crime.get("description")
    }
