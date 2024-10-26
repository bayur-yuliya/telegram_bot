import telebot
from telebot import types
import webbrowser

from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=["photo"])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    button_site = types.InlineKeyboardButton(
            "Перейти на сайт",
            url="https://translate.google.com/?sl=en&tl=ru&op=translate",
        )
    button_delete = types.InlineKeyboardButton("Удалить фото", callback_data="delete")
    button_edit = types.InlineKeyboardButton("Изменить текст", callback_data="edit")
    markup.row(button_site)
    markup.row(button_delete, button_edit)
    bot.reply_to(message, "Какое красивое фото!", reply_markup=markup)


@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, "Text")


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(
        message.chat.id, "<b>Help</b> <em><u>information</u></em>", parse_mode="html"
    )


@bot.message_handler(commands=["info_user"])
def info_user(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=["site", "website"])
def site(message):
    webbrowser.open("https://translate.google.com/?sl=en&tl=ru&op=translate")


@bot.message_handler(commands=["user_name"])
def user_name(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}")


@bot.message_handler()
def info(message):
    if message.text == "привет":
        bot.send_message(
            message.chat.id,
            f"Привет, {message.from_user.first_name} {message.from_user.last_name}",
        )
    elif message.text == "id":
        bot.reply_to(message, f"ID: {message.from_user.id}")


bot.infinity_polling()
