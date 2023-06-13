import logging
import asyncio
from aiohttp.web import Application, run_app
from dispatcher import dp, bot, redis, storage
from settings import WEBHOOK_PATH, WEBHOOK_DOMAIN, LOCAL_MODE
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from db import init_database, stop_database

logging.basicConfig(level=logging.DEBUG)


@dp.message()
async def start(message: types.Message, state: FSMContext):
    await message.answer(
        "Deployment Test", parse_mode="markdown"
    )


# INITIALIZATION
# Prepare function for starting bot
async def _on_startup(app):
    await bot.set_webhook(WEBHOOK_DOMAIN + WEBHOOK_PATH)


async def _on_shutdown(app):
    await bot.delete_webhook()
    await storage.close()


async def _init(*_):
    print("Init database")
    await init_database()


async def _shutdown(*_):
    print("Shutdown database")
    await stop_database()


async def _start_polling():
    await _init()
    await dp.start_polling(bot, handle_as_tasks=False)
    await _shutdown()


if __name__ == "__main__":
    print("Start bot")
    if LOCAL_MODE:
        print("Start polling")
        asyncio.run(_start_polling())
    else:
        print("Start webhook")
        app = Application()
        setup_application(app, dp)
        app.on_startup.append(_on_startup)
        app.on_startup.append(_init)

        app.on_shutdown.append(_on_shutdown)
        app.on_shutdown.append(_shutdown)

        handler = SimpleRequestHandler(dp, bot)

        app.router.add_route("*", WEBHOOK_PATH, handler)

        run_app(app, port=8000)
