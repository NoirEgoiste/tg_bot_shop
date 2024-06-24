import logging
import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from app.database.models import async_main
from app.handlers import router
from app.admin import admin as admin_router


async def main():
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(admin_router, router)

    await dp.start_polling(bot)    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Ctrl+C pressed. Exiting.')
