from fastapi import FastAPI, HTTPException
from bson.objectid import ObjectId
from db import get_weather_collection
from models import WeatherDataIn, WeatherDataOut
from pymongo.errors import PyMongoError

app = FastAPI()
collection = get_weather_collection()


def document_to_model(doc) -> WeatherDataOut:
    """Helper to convert MongoDB doc to Pydantic model"""
    return WeatherDataOut(
        id=str(doc["_id"]),
        name=doc["name"],
        main=doc["main"],
        wind=doc["wind"]
    )


@app.get("/weather/", response_model=list[WeatherDataOut])
def get_all_weather():
    weather_list = []
    for item in collection.find():
        weather_list.append(document_to_model(item))
    return weather_list


@app.post("/weather/", response_model=WeatherDataOut)
def create_weather(data: WeatherDataIn):
    result = collection.insert_one(data.model_dump())

    data.model_dump(exclude_unset=True)

    created = collection.find_one({"_id": result.inserted_id})
    return document_to_model(created)


@app.put("/weather/{id}", response_model=WeatherDataOut)
def update_weather(id: str, data: WeatherDataIn):
    update_result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data.dict()}
    )
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Weather data not found")
    updated = collection.find_one({"_id": ObjectId(id)})
    return document_to_model(updated)


@app.delete("/weather/{id}")
def delete_weather(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return {"message": "Deleted"}


@app.get("/weather/{weather_id}")
def get_weather_by_id(weather_id: str):
    if not ObjectId.is_valid(weather_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format.")
    
    try:
        data = collection.find_one({"_id": ObjectId(weather_id)})
        if data is None:
            raise HTTPException(status_code=404, detail="Weather data not found.")
        data["_id"] = str(data["_id"])
        return data
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database error.")
