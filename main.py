from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ml_service import ml_matcher
from database import crimes_collection, ncrb_collection
import uuid

app = FastAPI(title="Crime Analysis ML API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Starting up and training ML model from database...")
    success = await ml_matcher.load_and_train()
    if success:
        print("ML Model successfully trained!")

class CrimeQuery(BaseModel):
    latitude: float
    longitude: float
    crime_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

class NewIncident(BaseModel):
    crime_type: str
    latitude: float
    longitude: float

@app.post("/admin/login")
async def admin_login(req: LoginRequest):
    if req.username == "admin" and req.password == "police123":
        return {"token": "police_secure_token_123"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/ncrb_stats")
async def get_ncrb_stats():
    cursor = ncrb_collection.find({}, {"_id": 0})
    data = await cursor.to_list(length=None)
    sorted_data = sorted(data, key=lambda x: x.get("crimes_2022", 0), reverse=True)
    return {"states": sorted_data}

@app.get("/chicago_stats")
async def get_chicago_stats():
    # Provide an aggregate of crime types
    pipeline = [
        {"$group": {"_id": "$crime_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    cursor = crimes_collection.aggregate(pipeline)
    data = await cursor.to_list(length=None)
    # top 7 for a pie chart or bar chart
    return {"aggregates": data[:7]}

@app.post("/add_incident")
async def add_incident(incident: NewIncident):
    # Insert new incident directly into the chicago structurally identical collection
    await crimes_collection.insert_one({
        "case_number": f"NEW-{str(uuid.uuid4())[:8]}",
        "date": "Just Now",
        "crime_type": incident.crime_type,
        "description": "Live Field Report",
        "location_desc": "Street",
        "latitude": incident.latitude,
        "longitude": incident.longitude
    })
    
    return {"message": "Incident reported successfully."}

@app.post("/retrain")
async def retrain_model():
    print("Retraining triggered...")
    success = await ml_matcher.load_and_train()
    if success:
        return {"message": "Neural Core Retrained."}
    raise HTTPException(status_code=500, detail="Retraining failed.")

@app.post("/predict_matches")
async def predict_matches(query: CrimeQuery):
    if not ml_matcher.is_trained:
        raise HTTPException(status_code=503, detail="ML model is not yet trained or no data available.")
        
    matches = ml_matcher.find_matches(query.latitude, query.longitude, query.crime_type)
    return {"matches": matches}

@app.get("/stats")
async def get_stats():
    count = await crimes_collection.count_documents({})
    return {"total_records": count, "model_trained": ml_matcher.is_trained}

@app.get("/")
async def root():
    return {"message": "Welcome to A.R.E.S. API V2"}
