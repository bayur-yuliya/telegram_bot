import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import WebAppInfo

from config import TOKEN, URL


dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):

    bt = [[types.KeyboardButton(text='hi', web_app=WebAppInfo(url=URL))]]
    markup = types.ReplyKeyboardMarkup(keyboard=bt)
    await message.answer('Open app', reply_markup=markup)


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
