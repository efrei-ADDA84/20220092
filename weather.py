# Imports
import os
import requests
from fastapi import FastAPI

# Get api key from env
api_key = os.environ.get("API_KEY")

# Create API
app = FastAPI()


# Create route
@app.get("/")
def weather(lat: float, lon: float, api_key: str = os.environ.get("API_KEY")):
    # Create URL
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"

    # Request data
    response = requests.get(url)

    # If valid response
    if response.status_code == 200:
        # Wrap it
        data = response.json()
        city = data["name"]
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]

        # Return it
        return {"city": city, "weather": weather, "temperature": temp}
    else:
        # Return an error
        return {"error": "Error while requesting data from API."}
