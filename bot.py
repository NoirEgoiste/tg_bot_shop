import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats


from bot_commands_list import private
from config import TOKEN
from app.database.models import async_main
from app.handlers.user_handlers import user
from app.handlers.admin_handlers import admin as admin_router
from app.handlers.user_group import group

ALLOWED_UPDATES = ["message", "edit_message", "callback_query"]


async def main():
    await async_main()
    bot = Bot(token=TOKEN)

    dp = Dispatcher()
    dp.include_routers(admin_router, user, group)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        commands=private,
        scope=BotCommandScopeAllPrivateChats()
    )
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Ctrl+C pressed. Exiting.')
