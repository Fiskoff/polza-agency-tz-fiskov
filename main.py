import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from fastapi_app.routers import api_router
from aiogram_app.handlers import tg_router


logger = logging.getLogger(__name__)

async def run_bot():
    bot = Bot(token=settings.tg.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(tg_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

async def run_api():
    app = FastAPI()
    app.include_router(api_router, prefix=settings.api.prefix)

    config = uvicorn.Config(
        app,
        host=settings.api.host,
        port=settings.api.port,
        loop="asyncio",
        reload=True
    )
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    settings.log.configure_logging()

    await asyncio.gather(
        run_bot(),
        run_api()
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Finished")