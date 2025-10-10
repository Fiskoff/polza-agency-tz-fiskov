import os
import re
import tempfile
import logging
from typing import Set, Dict, Pattern
from fastapi import UploadFile, HTTPException

import fitz
import docx

from fastapi_app.data.skills_loader import load_skills
from fastapi_app.schemas import SkillsResponse


MAX_FILE_SIZE: int = 10 * 1024 * 1024

COMPILED_PATTERNS: Dict[str, Pattern] = None


def _load_and_compile_patterns() -> Dict[str, Pattern[str]]:
    """
        Загружает и компилирует регулярные выражения для поиска навыков
        Компилирует только один раз и кэширует результат
    """
    global COMPILED_PATTERNS
    if COMPILED_PATTERNS is None:
        skill_patterns: Dict[str, str] = load_skills()
        COMPILED_PATTERNS = {
            skill: re.compile(pattern, re.IGNORECASE)
            for skill, pattern in skill_patterns.items()
        }
    return COMPILED_PATTERNS


def secure_filename(filename: str) -> str:
    """Очищает имя файла от потенциально опасных символов"""
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)


class ApiServices:
    """ Класс, предоставляющий бизнес-логику для извлечения навыков из текста и файлов"""

    @staticmethod
    def extract_skills_from_text(text: str) -> Set[str]:
        """Извлекает навыки из текста, используя заранее скомпилированные регулярные выражения"""
        try:
            if not text or not text.strip():
                return set()

            compiled_patterns: Dict[str, Pattern[str]] = _load_and_compile_patterns()
            found_skills: Set[str] = set()

            for skill, compiled_pattern in compiled_patterns.items():
                if compiled_pattern.search(text):
                    found_skills.add(skill)

            return found_skills
        except Exception as e:
            logging.error(f"Ошибка при анализе текста: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при анализе текста")

    @staticmethod
    def analyze_text_for_skills(text: str) -> SkillsResponse:
        """Анализирует текст и возвращает модель ответа с найденными навыками"""
        try:
            found_skills: Set[str] = ApiServices.extract_skills_from_text(text)
            return SkillsResponse(skills=list(found_skills))
        except Exception as e:
            logging.error(f"Ошибка при анализе текста: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при анализе текста")

    @staticmethod
    def extract_text_from_file(file_path: str) -> str:
        """Извлекает текст из файла PDF или DOCX"""
        if file_path.endswith('.pdf'):
            try:
                doc = fitz.open(file_path)
                text: str = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                return text
            except Exception:
                raise HTTPException(status_code=400, detail="Некорректный PDF файл")
        elif file_path.endswith('.docx'):
            try:
                doc = docx.Document(file_path)
                return "\n".join([p.text for p in doc.paragraphs])
            except Exception:
                raise HTTPException(status_code=400, detail="Некорректный DOCX файл")
        else:
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")

    @staticmethod
    async def process_uploaded_file(file: UploadFile) -> SkillsResponse:
        """Обрабатывает загруженный файл (PDF или DOCX) и возвращает найденные навыки."""
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Файл слишком большой")

        if file.content_type not in ["application/pdf",
                                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            raise HTTPException(status_code=400, detail="Файл должен быть PDF или DOCX")

        suffix: str = os.path.splitext(secure_filename(file.filename))[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content: bytes = await file.read()
            temp_file.write(content)
            temp_path: str = temp_file.name

        try:
            text: str = ApiServices.extract_text_from_file(temp_path)
            found_skills: Set[str] = ApiServices.extract_skills_from_text(text)
            return SkillsResponse(skills=list(found_skills))
        except Exception as e:
            logging.error(f"Ошибка при обработке файла: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при обработке файла")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)