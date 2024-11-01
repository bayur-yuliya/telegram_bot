from telebot import TeleBot
from config import TOKEN, API
import requests
import json

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, рад тебя видеть! Напиши название города")


@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text.strip().lower()
    weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric"
    )
    data = json.loads(weather.text)
    temp = data["main"]["temp"]
    bot.reply_to(message, f"Температура сейчас в этом городе: {temp}")

    image = "cold.jpg" if temp < 10.0 else "hot.png"
    file = open("img/" + image, "rb")
    bot.send_photo(message.chat.id, file)


bot.polling(non_stop=True)
