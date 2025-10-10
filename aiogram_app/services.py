import os
import asyncio
import logging

import fitz
import docx
from aiogram import Bot
from aiogram.types import Message


class BotService:
    """ Класс, предоставляющий бизнес-логику для извлечения навыков из текста и файлов"""

    @staticmethod
    def extract_text_from_file(file_name: str) -> str:
        """Извлекает текст из PDF или DOCX файла"""
        text = ""

        if file_name.endswith('.pdf'):
            doc = fitz.open(file_name)
            for page in doc:
                text += page.get_text()
            doc.close()

        elif file_name.endswith('.docx'):
            doc = docx.Document(file_name)
            text = "\n".join([p.text for p in doc.paragraphs])

        return text

    @staticmethod
    async def process_document_message(message: Message, bot: Bot) -> str | None:
        """Обрабатывает загруженный документ PDF/DOCX, извлекает текст и удаляет файл"""
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        original_filename = message.document.file_name
        safe_filename = f"temp_{hash(original_filename)}_{original_filename}"
        safe_filepath = os.path.join("temp", safe_filename)

        os.makedirs("temp", exist_ok=True)

        try:
            await bot.download_file(file_path, safe_filepath)

            loop = asyncio.get_event_loop()
            text = await loop.run_in_executor(None, BotService.extract_text_from_file, safe_filepath)
            return text

        except Exception as e:
            logging.error(f"Ошибка при обработке файла: {e}")
            return None

        finally:
            if os.path.exists(safe_filepath):
                os.remove(safe_filepath)