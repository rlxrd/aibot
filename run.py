import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from app.user import user
from app.admin import admin
from app.database.models import create_tables


async def main():
    bot = Bot(token=TOKEN)
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
