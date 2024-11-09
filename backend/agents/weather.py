# /backend/agents/weather.py
import requests

class WeatherAgent:
    def fetch_weather(self, city, date):
        """Fetch weather information for a given city and date."""
        api_url = f"http://api.weatherapi.com/v1/forecast.json?key=your_api_key&q={city}&dt={date}"
        response = requests.get(api_url)
        weather_data = response.json()
        return weather_data['forecast']['forecastday'][0]['day']['condition']['text']
