import requests
import json
import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read credentials and parameters from .env
API_KEY = os.getenv("API_KEY")
LOCATION = os.getenv("LOCATION")
LAT = os.getenv("LAT")
LON = os.getenv("LON")
URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}"

def fetch_weather():
    """Fetch weather data for a specified location."""
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return {
            "date": str(datetime.datetime.now()),
            "location": LOCATION,
            "temperature": round(data["main"]["temp"] - 273.15, 2),  # Convert Kelvin to Celsius
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
    else:
        return {"error": "Failed to fetch weather data"}

def save_data(data, filename="weather_data.json"):
    """Save weather data to a JSON file as an array of objects."""
    try:
        # Try to read the existing data from the file
        with open(filename, "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        existing_data = []
    except json.JSONDecodeError:
        # If the file exists but is not valid JSON, start with an empty list
        existing_data = []

    # Append the new data
    existing_data.append(data)

    # Write the updated data back to the file
    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)

if __name__ == "__main__":
    weather_data = fetch_weather()
    save_data(weather_data)
    print("Weather data saved:", weather_data)
