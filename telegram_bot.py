import telebot
from telebot import types
import webbrowser
import sqlite3

from config import TOKEN

bot = telebot.TeleBot(TOKEN)
name = None


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    button_site = types.KeyboardButton("Перейти на сайт")
    button_delete = types.KeyboardButton("Удалить фото")
    button_edit = types.KeyboardButton("Изменить фото")
    markup.row(button_site)
    markup.row(button_delete, button_edit)
    bot.send_message(message.chat.id, "Какое красивое фото!", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == "Перейти на сайт":
        webbrowser.open("https://translate.google.com/?sl=en&tl=ru&op=translate")
    elif message.text == "Удалить фото":
        bot.send_message(message.chat.id, "Delete photo")
    elif message.text == "Изменить фото":
        bot.send_message(message.chat.id, "Edit photo")


@bot.message_handler(commands=["send_photo"])
def send_photo(message):
    file = open("./photo.jpg", "rb")
    bot.send_photo(message.chat.id, file)


@bot.message_handler(commands=["db"])
def db(message):
    conn = sqlite3.connect("telebot.sql")
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), password varchar(50))"
    )
    conn.commit()

    cur.close()
    conn.close()

    bot.send_message(
        message.chat.id, "Привет, сейчас зарегистрируем данные. Введите имя: "
    )
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Введите пароль: ")
    bot.register_next_step_handler(message, user_password)


def user_password(message):
    password = message.text.strip()
    conn = sqlite3.connect("telebot.sql")
    cur = conn.cursor()

    cur.execute(
        'INSERT INTO users (name, password) VALUES ("%s", "%s")' % (name, password)
    )
    conn.commit()

    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Список пользователей", callback_data="user_list")
    )

    bot.send_message(
        message.chat.id, "Пользователь зарегистрирован", reply_markup=markup
    )


@bot.callback_query_handler(func=lambda callback: True)
def user_list(callback):
    conn = sqlite3.connect("telebot.sql")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    info = ""
    for user in users:
        info += f"Имя: {user[1]}, пароль: {user[2]}\n"

    cur.close()
    conn.close()

    bot.send_message(callback.message.chat.id, info)


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


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == "edit":
        bot.edit_message_text(
            "Edit text", callback.message.chat.id, callback.message.message_id
        )


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
