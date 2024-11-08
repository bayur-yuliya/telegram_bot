from telebot import TeleBot, types
from currency_converter import CurrencyConverter

from config import TOKEN

bot = TeleBot(TOKEN)
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Введите сумму: ')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат, впишите сумму: ')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('EUR/GBP', callback_data='eur/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение: ', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите конвертацию каких валют сделать', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Число должно быть больше 0. Введите данные заново: ")
        bot.register_next_step_handler(message, summa)
        return


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Результат конвертации: {round(res, 2)}. Можете продолжить')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару валюты через слеш')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Результат конвертации: {round(res, 2)}. Можете продолжить')
        bot.register_next_step_handler(message, summa)
    except IndexError:
        bot.send_message(message.chat.id, 'Что-то не так, впишите значения заново')
        bot.register_next_step_handler(message, summa)

bot.polling(non_stop=True)
