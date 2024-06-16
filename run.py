import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.user import user
from app.admin import admin
from app.database.models import create_tables

from config import TOKEN


async def main():
    bot = Bot(token=TOKEN,
              #default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
              )
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.include_routers(user, admin)
    await dp.start_polling(bot)


async def on_startup(dispatcher):
    await create_tables()
    print('BOT STARTED')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
