from pydantic import BaseModel
from typing import List, Dict

class MainWeather(BaseModel):
    temp: float
    humidity: int

class Wind(BaseModel):
    speed: float

class WeatherData(BaseModel):
    name: str  # city name
    main: MainWeather
    wind: Wind
