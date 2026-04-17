import requests
from geopy.geocoders import Nominatim
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import threading

now = datetime.now()

def geocode_location(location_str):
    """Geocode location string to (latitude, longitude)."""
    geolocator = Nominatim(user_agent='weather_app')
    location = geolocator.geocode(location_str)
    if location is None:
        raise ValueError("Invalid location. Please check spelling (e.g., 'New York, NY').")
    return location.latitude, location.longitude

def fetch_weather_data(latitude, longitude):
    """Fetch weather forecast data from NWS API."""
    url = f'https://api.weather.gov/points/{latitude},{longitude}'
    response = requests.get(url)
    response.raise_for_status()
    init_data = response.json()
    forecast_url = init_data['properties']['forecast']
    forecast_response = requests.get(forecast_url)
    forecast_response.raise_for_status()
    return forecast_response.json()

def format_period(period):
    """Format a single weather period for display."""
    return f"""Name: {period['name']}
Temperature: {period['temperature']} {period['temperatureUnit']}
Wind Speed: {period['windSpeed']}
Wind Direction: {period['windDirection']}
Short Forecast: {period['shortForecast']}
Detailed Forecast: {period['detailedForecast']}
{'-' * 100}, '\n'"""

class WeatherAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App GUI")
        self.root.geometry("700x600")

        # Location input
        tk.Label(root, text="Enter location (e.g., 'City, State'):", font=('Arial', 12)).pack(pady=10)
        self.location_entry = tk.Entry(root, width=40, font=('Arial', 12))
        self.location_entry.pack(pady=5)
        self.location_entry.bind('<Return>', lambda e: self.fetch_current())

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        self.current_btn = tk.Button(btn_frame, text="Get Current Weather", command=self.fetch_current, bg='lightblue', font=('Arial', 11))
        self.current_btn.pack(side=tk.LEFT, padx=5)
        self.forecast_btn = tk.Button(btn_frame, text="Get 7-Day Forecast", command=self.fetch_forecast, bg='lightgreen', font=('Arial', 11))
        self.forecast_btn.pack(side=tk.LEFT, padx=5)
        self.clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_output, bg='lightcoral', font=('Arial', 11))
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Status
        self.status_label = tk.Label(root, text="Ready", fg='green', font=('Arial', 10))
        self.status_label.pack(pady=5)

        # Output
        self.output_text = scrolledtext.ScrolledText(root, width=80, height=25, font=('Arial', 10))
        self.output_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def update_status(self, msg, fg='black'):
        self.status_label.config(text=msg, fg=fg)
        self.root.update()

    def fetch_in_thread(self, fetch_func):
        def thread_func():
            try:
                self.current_btn.config(state='disabled')
                self.forecast_btn.config(state='disabled')
                self.update_status("Loading...", 'orange')
                result = fetch_func()
                self.root.after(0, lambda: self.display_result(result))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.root.after(0, self.enable_buttons)
        threading.Thread(target=thread_func, daemon=True).start()

    def fetch_current(self):
        def get_current():
            loc_str = self.location_entry.get().strip()
            if not loc_str:
                raise ValueError("Please enter a location.")
            lat, lon = geocode_location(loc_str)
            data = fetch_weather_data(lat, lon)
            periods = data['properties']['periods']
            return format_period(periods[0])
        self.fetch_in_thread(get_current)

    def fetch_forecast(self):
        def get_forecast():
            loc_str = self.location_entry.get().strip()
            if not loc_str:
                raise ValueError("Please enter a location.")
            lat, lon = geocode_location(loc_str)
            data = fetch_weather_data(lat, lon)
            periods = data['properties']['periods']
            output = f"Current Time: {now}\n"
            for period in periods:
                output += format_period(period)
            return output
        self.fetch_in_thread(get_forecast)

    def display_result(self, text):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.update_status("Ready", 'green')

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.update_status("Cleared", 'blue')

    def enable_buttons(self):
        self.current_btn.config(state='normal')
        self.forecast_btn.config(state='normal')
        self.update_status("Ready", 'green')

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherAppGUI(root)
    root.mainloop()
