import requests

API_KEY = '0ba3c1e11989038f5aaf057d2eabff17'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_weather(city='Canberra'):
    try:
        response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY, 'units': 'metric'})
        weather_data = response.json()
        if weather_data.get('cod') != 200:
            return "I couldn't retrieve the weather information at this moment."
        weather_desc = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        return f"The weather in {city} is currently {weather_desc} with a temperature of {temperature}°C."
    except Exception as e:
        return f"An error occurred while fetching the weather information: {e}"
