import requests

def get_weather():
    api_key = "0ba3c1e11989038f5aaf057d2eabff17"  # Your OpenWeatherMap API key
    city_name = "Canberra"  # City name
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    weather_data = response.json()
    if weather_data["cod"] != "404":
        main = weather_data["main"]
        weather = weather_data["weather"][0]
        temperature = main["temp"]
        description = weather["description"]
        return f"The weather in {city_name} is currently {description} with a temperature of {temperature - 273.15:.2f}°C."
    else:
        return "Sorry, I couldn't retrieve the weather information."
