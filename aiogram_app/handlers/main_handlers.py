from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_app.handlers.resume_handler import resume_router
from aiogram_app.handlers.search_handler import search_router


tg_router = Router()
tg_router.include_router(resume_router)
tg_router.include_router(search_router)

@tg_router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start. Вернёт список команд"""
    await message.answer("Команды:\n/resume - для загрузки резюме\n/search - поиска вакансий")