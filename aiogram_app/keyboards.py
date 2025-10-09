from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def get_vacancy_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for i in range(1, 4):
        builder.button(text=f"Вакансия {i}", callback_data=f"vacancy_{i}")
    builder.adjust(1)

    return builder.as_markup()

def get_back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад к вакансиям", callback_data="back_to_vacancies")
    return builder.as_markup()