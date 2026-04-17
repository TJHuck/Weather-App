import requests
from geopy.geocoders import Nominatim
import json
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

## Global Vars
now = datetime.now()

# Define the function to fetch weather data
def fetch_weather():
    url = f'https://api.weather.gov/points/{latitude},{longitude}'
    response = requests.get(url)
    init_response_data = response.json()
    forecast_url = init_response_data['properties']['forecast']
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()
    seven_day_choice = input('Do you want to see the 7-day forecast? (yes/no): ')
    if seven_day_choice.lower() == 'yes' or seven_day_choice.lower() == 'y' or seven_day_choice.lower() == 'YES':
        for period in forecast_data['properties']['periods']:
            print('Current Time: ' , now)
            if forecast_data['properties']['periods'].index(period) == 0:
                print('-' * 100)
            print(f'Name: {period['name']}')
            print(f'Temperature: {period['temperature']} {period['temperatureUnit']}')
            print(f'Wind Speed: {period['windSpeed']}')
            print(f'Wind Direction: {period['windDirection']}')
            print(f'Short Forecast: {period['shortForecast']}')
            print(f'Detailed Forecast: {period['detailedForecast']}')
            print('-' * 100)
    elif seven_day_choice.lower() == 'no' or seven_day_choice.lower() == 'n' or seven_day_choice.lower() == 'NO':
        print('-' * 100)
        print('Current Time: ' , now)
        current_period = forecast_data['properties']['periods'][0]
        print(f'Name: {current_period['name']}')
        print(f'Temperature: {current_period['temperature']} {current_period['temperatureUnit']}')
        print(f'Wind Speed: {current_period['windSpeed']}')
        print(f'Wind Direction: {current_period['windDirection']}')
        print(f'Short Forecast: {current_period['shortForecast']}')
        print(f'Detailed Forecast: {current_period['detailedForecast']}')
        print('-' * 100)
    else:
        print('Invalid choice. Please enter "yes" or "no".')



loc_input = True

while loc_input == True:
    user_loc_input = input('Enter your location (e.g., "City, State"): ')
    try:
        if user_loc_input == str:
            continue
        loc_input = False
    except:
        print('Invalid input. Please enter a valid location.')


geolocator = Nominatim(user_agent='weather_app')
location = geolocator.geocode(user_loc_input)
latitude = location.latitude
longitude = location.longitude

fetch_weather()
