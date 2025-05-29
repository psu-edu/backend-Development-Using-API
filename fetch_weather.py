import os
import requests
from models import WeatherData
from db import save_to_mongo
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Philadelphia"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()

try:
    validated_data = WeatherData(**data)
    print("✅ Valid data:", validated_data)
    save_to_mongo(validated_data.dict())
except Exception as e:
    print("❌ Validation or DB Error:", e)
