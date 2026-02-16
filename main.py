import asyncio
import logging
import os

# Aiogram Imports #
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeDefault

# My Imports #
from config import Settings
from handlers.user_handler import user_private_router
from bot_commands.bot_commands_list import private

from database.engine import create_db, drop_db, session_maker
from middlewares.db_middleware import DataBaseSession
from middlewares.user_context_middleware import UserContextMiddleware

token = Settings.TOKEN

bot = Bot(token=token)
dp = Dispatcher()

dp.include_router(user_private_router)


async def startup(bot):
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def shutdown(bot):
    print("Bot down")


async def main():
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.update.middleware(UserContextMiddleware())   # !!! AFTER DataBaseSession for session already has been created !!!
    await bot.set_my_commands(commands=private, scope=BotCommandScopeDefault())
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


