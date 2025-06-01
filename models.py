from pydantic import BaseModel
from typing import Optional

class WeatherMain(BaseModel):
    temp: float
    humidity: int

class WeatherWind(BaseModel):
    speed: float

class WeatherDataIn(BaseModel):
    name: str
    main: WeatherMain
    wind: WeatherWind

class WeatherDataOut(WeatherDataIn):
    id: Optional[str]  # MongoDB _id mapped as string
