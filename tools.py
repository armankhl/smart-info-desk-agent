# tools.py
import os
import requests

def get_weather(location: str) -> str:
    """Fetches the current weather for a given location."""
    api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        # Extract and format the relevant information
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"The current weather in {location} is {temp}°C with {weather_desc}."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"