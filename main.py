import telebot
import requests
import datetime
from data import tg_bot_token, open_weather_token

bot = telebot.TeleBot(tg_bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>, Напиши мне название города, и я отправлю сводку погоды!'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Введи город!")

@bot.message_handler()
def get_weather(message):
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
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric")
        data = r.json()

        city = data["name"]
        current_temp = data["main"]["temp"]
        max_temp = data["main"]["temp_max"]
        min_temp = data["main"]["temp_min"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            sm = code_to_smile[weather_description]
        else:
            sm = "Посмотри в окно, не пойму, что там за погода!"

        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - \
                            datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        bot.send_message(message.chat.id, f"Текущее время <u>{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</u>\n"
              f"Погода в городе: {city}\nТемпература: {current_temp} C° {sm}\nМаксимальная температура: {max_temp} C°\n"
              f"Минимальная температура: {min_temp} C°\n"
              f"Влажность: {humidity} %\nСкорость ветра: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n\n"
              f"<b>Удачи!</b>", parse_mode='html')


    except:
        bot.send_message(message.chat.id, "🛑 <u>Проверьте название города</u> 🛑", parse_mode='html')

bot.polling(none_stop=True)
