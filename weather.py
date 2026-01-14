# weather.py
import requests
from config import WEATHER_API_KEY, CITY, UNITS

def get_weather():
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={CITY}&appid={WEATHER_API_KEY}&units={UNITS}"
        )
        data = requests.get(url, timeout=5).json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].title()
        return f"{CITY}: {temp}°C | {desc}"
    except:
        return "Weather: Unavailable"

