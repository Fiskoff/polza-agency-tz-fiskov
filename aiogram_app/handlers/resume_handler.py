from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from aiogram_app.services import BotService


resume_router = Router()

class ResumeStates(StatesGroup):
    """FSM для загрузки резюме"""
    waiting_for_resume = State()


@resume_router.message(Command("resume"))
async def cmd_resume(message: Message, state: FSMContext):
    """Обработчик команды /resume. Запрашивает у пользователя файл резюме"""
    await state.set_state(ResumeStates.waiting_for_resume)
    await message.answer("Отправьте файл резюме в формате PDF или DOCX")

@resume_router.message(
    ResumeStates.waiting_for_resume,
    lambda msg: msg.document and msg.document.mime_type in [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
)
async def handle_document(message: Message, bot, state: FSMContext):
    """Обработчик загруженного документа PDF/DOCX. Извлекает текст из файла и отправляет пользователю"""
    text = await BotService.process_document_message(message, bot)

    if text:
        await message.answer(f"Резюме:\n\n{text}")
    else:
        await message.answer("Произошла ошибка при обработке файла.")

    await state.clear()

@resume_router.message(Command("cancel"), ResumeStates.waiting_for_resume)
async def cancel_resume(message: Message, state: FSMContext):
    """Обработчик команды /cancel. Отменяет загрузку резюме и очищает состояние"""
    await state.clear()
    await message.answer("Загрузка резюме отменена")

@resume_router.message(ResumeStates.waiting_for_resume)
async def handle_not_document(message: Message):
    """Обработчик, если пользователь отправил не документ. Отправляет пользователю инструкцию"""
    await message.answer("Отправьте PDF или DOCX файл.\n\nДля отмены используйте /cancel")