import os
import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from aiogram_app.services import BotService


resume_router = Router()

class ResumeStates(StatesGroup):
    waiting_for_resume = State()


@resume_router.message(Command("resume"))
async def cmd_resume(message: Message, state: FSMContext):
    await state.set_state(ResumeStates.waiting_for_resume)
    await message.answer("Отправьте файл резюме в формате PDF или DOCX")

@resume_router.message(ResumeStates.waiting_for_resume, lambda msg: msg.document and msg.document.mime_type in [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
)
async def handle_document(message: Message, bot, state: FSMContext):
    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    file_name = f"temp_{message.document.file_name}"
    await bot.download_file(file_path, file_name)

    loop = asyncio.get_event_loop()
    text = await loop.run_in_executor(None, BotService.extract_text_from_file, file_name)
    await message.answer(f"Резюме:\n\n{text}")

    os.remove(file_name)
    await state.clear()

@resume_router.message(Command("cancel"), ResumeStates.waiting_for_resume)
async def cancel_resume(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Загрузка резюме отменена")

@resume_router.message(ResumeStates.waiting_for_resume)
async def handle_not_document(message: Message):
    await message.answer("Отправьте PDF или DOCX файл.\n\nДля отмены используйте /cancel")