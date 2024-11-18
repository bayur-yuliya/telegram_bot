import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart

import config

bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(Command('pay'))
async def invoice(message: types.Message):
    await bot.send_invoice(chat_id=message.chat.id,
                           title='Покупка в телеграм магазине',
                           description="Покупка тестовая",
                           payload="invoice",
                           provider_token=config.PAYMENT_TOKEN,
                           currency='USD',
                           prices=[types.LabeledPrice(label='Покупка', amount=145)],
                           request_timeout=40)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
