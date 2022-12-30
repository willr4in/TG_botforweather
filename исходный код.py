# исходник, возможны отличия

import requests
import datetime
from pprint import pprint
from data import open_weather_token

def get_weather(city, open_weather_token):

    code_to_smile = {
        "Clear": "Ясно ☀",
        "Clouds": "Облачно 🌥️",
        "Rain": "Дождь 🌧️",
        "Drizzle": "Дождь 🌧️",
        "Thunderstorm": "Гроза 🌩️",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")
        data = r.json()
        #pprint(data)

        city = data["name"]
        current_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            sm = code_to_smile[weather_description]
        else:
            sm = "Посмотри в окно, не пойму, что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - \
                            datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f"Погода в городе: {city}\nТемпература: {current_weather} C° {sm}\n"
              f"Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n\n"
              f"Хорошего дня!")


    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def main():
    city = input("Введите город: ")
    get_weather(city, open_weather_token)

if __name__ == '__main__':
    main()