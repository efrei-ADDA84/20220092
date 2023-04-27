# Imports
import os
import requests

# Get api key from env
api_key = os.environ.get("API_KEY")

# Get coordinates from env
lat = os.environ.get("LAT")
lon = os.environ.get("LONG")

# Create URL
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"

# Send request and write response
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    city = data["name"]
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    print(f"{city}'s current weather is {weather}. It is {temp}°C.")
else:
    print("Error while requesting data from API.")
