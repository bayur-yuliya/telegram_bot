import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from currency_converter import CurrencyConverter

from config import TOKEN


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
currency = CurrencyConverter()

amount = 0


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer('Привет! Введите сумму для конвертации:')


@dp.message()
async def get_amount(message: types.Message):

    try:
        global amount
        amount = float(message.text.strip())

        if amount <= 0:
            raise ValueError("Amount must be positive.")

    except ValueError:
        await message.answer('Неверный формат. Введите положительное число:')
        return

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='USD/EUR', callback_data='usd/eur'),
        ],
        [
            InlineKeyboardButton(text='EUR/USD', callback_data='eur/usd'),
        ],
        [
            InlineKeyboardButton(text='EUR/GBP', callback_data='eur/gbp'),
        ]
    ])
    await message.answer('Выберите конвертацию или введите свою пару:', reply_markup=markup)


@dp.callback_query()
async def handle_conversion(call: types.CallbackQuery):
    if amount <= 0:
        return

    base, target = call.data.upper().split('/')
    await convert_currency(call.message, base, target, amount)


async def convert_currency(message: types.Message, base: str, target: str, amount):
    await message.answer(f'{amount}')
    try:
        result = currency.convert(amount, base, target)
        await message.answer(f'Результат: {amount} {base} = {round(result, 2)} {target}')
        await message.answer('Введите новую сумму для конвертации или команду /start для начала:')
    except Exception as e:
        await message.answer(f'Ошибка конвертации: {str(e)}. Попробуйте еще раз:')


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
