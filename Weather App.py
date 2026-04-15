import requests
from geopy.geocoders import Nominatim
import json
import pandas as pd
# Define the function to fetch weather data
def fetch_weather():
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(url)
    data = response.json()
    readable_text = json.dumps(data, indent=2, sort_keys=True)
    print(readable_text)

loc_input = True

while loc_input == True:
    user_loc_input = input("Enter your location (e.g., 'City, State'): ")
    try:
        if user_loc_input == str:
            continue
        loc_input = False
    except:
        print("Invalid input. Please enter a valid location.")


geolocator = Nominatim(user_agent="")
location = geolocator.geocode(user_loc_input)
latitude = location.latitude
longitude = location.longitude

print(f"Latitude: {latitude}, Longitude: {longitude}")

fetch_weather()
