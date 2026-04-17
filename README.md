# Weather App

This is a weather app, it is a personal project, used to teach myself API calling and requests and implementation<br>

## How it works

There are two versions of this same program included in this repo. One, is the version that runs exclusivley in the terminal, and the other is a version that has a GUI implementation.<br><br>

Using the National Weather Service API Web Service (https://www.weather.gov/documentation/services-web-api) the program uses<br>
geopy and nominatim to convert the string user entry to useable Latitude and Longitude. Then, it uses those coordinates to <br> 
request the forecast from the NWS API. The response is a JSON file, so the program is designed to do some post-processing of the <br>
response to print it in a readable format.