from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from aiogram_app.keyboards import get_vacancy_keyboard, get_back_keyboard


search_router = Router()

@search_router.message(Command("search"))
async def cmd_search(message: Message):
    """Обработчик команды /search. Отправляет пользователю список вакансий с inline-клавиатурой"""
    await message.answer("Вакансий:", reply_markup=get_vacancy_keyboard())

@search_router.callback_query(lambda c: c.data.startswith("vacancy_"))
async def process_vacancy(callback_query: CallbackQuery):
    """Обработчик нажатия на кнопку вакансии. Отправляет информацию о вакансии и кнопку - Назад"""
    vacancy_num = callback_query.data.split("_")[1]
    await callback_query.answer(f"Вакансия:  {vacancy_num}!")
    await callback_query.message.edit_text(f"Название - {vacancy_num}\n\nСодержимое: текст текст текст", reply_markup=get_back_keyboard())

@search_router.callback_query(lambda c: c.data == "back_to_vacancies")
async def back_to_vacancies(callback_query: CallbackQuery):
    """Обработчик нажатия на кнопку "Назад к вакансиям". Возвращает пользователя к списку вакансий"""
    await callback_query.message.edit_text("Вот несколько вакансий:", reply_markup=get_vacancy_keyboard())