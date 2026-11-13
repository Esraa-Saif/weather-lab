import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherReport:
    """Stores and organizes weather data for a single city."""

    def __init__(self, city, country, temperature, feels_like,
                 humidity, pressure, wind_speed, description):
        self.city = city
        self.country = country
        self.temperature = temperature
        self.feels_like = feels_like
        self.humidity = humidity
        self.pressure = pressure
        self.wind_speed = wind_speed
        self.description = description

    @classmethod
    def from_json(cls, data):
        """Build a WeatherReport from the API's JSON response."""
        return cls(
            city=data["name"],
            country=data["sys"]["country"],
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            wind_speed=data["wind"]["speed"],
            description=data["weather"][0]["description"].title(),
        )

    def display(self):
        """Print a formatted summary."""
        line = "=" * 40
        print(line)
        print(f" Weather Report: {self.city}, {self.country}")
        print(line)
        print(f" Condition   : {self.description}")
        print(f" Temperature : {self.temperature:.1f} °C")
        print(f" Feels like  : {self.feels_like:.1f} °C")
        print(f" Humidity    : {self.humidity} %")
        print(f" Pressure    : {self.pressure} hPa")
        print(f" Wind speed  : {self.wind_speed} m/s")
        print(line)


def fetch_weather(city):
    """Call the API and return the parsed JSON (dict)."""
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params, timeout=10)

    if response.status_code == 401:
        raise RuntimeError("Invalid API key (or it is not activated yet).")
    if response.status_code == 404:
        raise RuntimeError(f"City '{city}' not found.")
    response.raise_for_status()

    return response.json()


def main():
    if not API_KEY:
        sys.exit("Error: OPENWEATHER_API_KEY not found. Check your .env file.")

    city = input("Enter city name: ").strip() or "Cairo"

    try:
        data = fetch_weather(city)
        report = WeatherReport.from_json(data)
        report.display()
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except RuntimeError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()