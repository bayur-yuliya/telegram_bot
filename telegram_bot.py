import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message()
async def info(message: types.Message):
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

dp.start_polling(dp)
