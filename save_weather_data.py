import requests
from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from models import WeatherDataIn, WeatherMain, WeatherWind

load_dotenv()

# Load env vars
MONGO_URI = os.getenv("MONGO_URI")
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["weather_db"]
collection = db["weather_data"]

# List of cities to fetch
cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Toronto", "Mumbai"]

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_data = WeatherDataIn(
            city=city,
            temperature=WeatherMain(temp=data["main"]["temp"]),
            wind=WeatherWind(speed=data["wind"]["speed"]),
            description=data["weather"][0]["description"]
        )
        return weather_data.dict()
    else:
        print(f"Failed to fetch data for {city}: {response.status_code}")
        return None   
    
def save_to_db(weather_data):
    if weather_data:
        existing = collection.find_one({"city": weather_data["city"]})
        if existing:
            collection.update_one({"city": weather_data["city"]}, {"$set": weather_data})
        else:
            collection.insert_one(weather_data)

# Fetch and store data for each city
for city in cities:
    weather = fetch_weather(city)
    save_to_db(weather)
    print(f"Saved: {city}")

