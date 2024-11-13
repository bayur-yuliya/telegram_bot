from telebot import TeleBot, types
from currency_converter import CurrencyConverter
from config import TOKEN

bot = TeleBot(TOKEN)
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Введите сумму для конвертации:')
    bot.register_next_step_handler(message, get_amount)


def get_amount(message):
    global amount
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError("Amount must be positive.")
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите положительное число:')
        bot.register_next_step_handler(message, get_amount)
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur'),
        types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd'),
        types.InlineKeyboardButton('EUR/GBP', callback_data='eur/gbp'),
        types.InlineKeyboardButton('Другая пара валют', callback_data='else')
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, 'Выберите конвертацию или введите свою пару:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_conversion(call):
    if call.data != 'else':
        base, target = call.data.upper().split('/')
        convert_currency(call.message, base, target)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару валюты в формате XXX/YYY:')
        bot.register_next_step_handler(call.message, get_custom_currency)


def get_custom_currency(message):
    try:
        base, target = message.text.upper().split('/')
        if base not in currency.currencies or target not in currency.currencies:
            raise ValueError("Unsupported currency")
        convert_currency(message, base, target)
    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный формат или неподдерживаемая валюта. Попробуйте еще раз:')
        bot.register_next_step_handler(message, get_custom_currency)


def convert_currency(message, base, target):
    try:
        result = currency.convert(amount, base, target)
        bot.send_message(message.chat.id, f'Результат: {amount} {base} = {round(result, 2)} {target}')
        bot.send_message(message.chat.id, 'Введите новую сумму для конвертации или команду /start для начала:')
        bot.register_next_step_handler(message, get_amount)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: {str(e)}. Попробуйте еще раз:')
        bot.register_next_step_handler(message, get_amount)


bot.polling(non_stop=True)
