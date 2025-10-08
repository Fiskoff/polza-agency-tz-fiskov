from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


tg_router = Router()

@tg_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Команды:\n/resume - для загрузки резюме\n/search - поиска вакансий")

@tg_router.message(Command("resume"))
async def cmd_resume(message: Message):
    await message.answer("Отправьте файл резюме в формате PDF или DOCX")