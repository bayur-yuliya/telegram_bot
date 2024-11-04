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
    amount = message.text.starip()

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
    btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
    btn3 = types.InlineKeyboardButton('EUR/UAH', callback_data='eur/uan')
    btn4 = types.InlineKeyboardButton('Другое значение: ', callback_data='else')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, 'Выберите конвертацию каких валют сделать')

bot.polling(non_stop=True)
