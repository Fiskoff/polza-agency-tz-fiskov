from fastapi import APIRouter, UploadFile, File, Body

from fastapi_app.schemas import SkillsResponse
from fastapi_app.services import ApiServices


api_router: APIRouter = APIRouter(prefix="/skills", tags=["Навыки"])

@api_router.post(
    "/extract",
    response_model=SkillsResponse,
    summary="Извлечение навыков из текста",
    description="""Принимает текст резюме или описания и извлекает из него список навыков.
    Текст должен быть передан в формате JSON в поле `text`.""",
    responses={
        200: {
            "description": "Список найденных навыков",
            "content": {
                "application/json": {
                    "example": {"skills": ["Python", "FastAPI", "PostgreSQL"]}
                }
            }
        },
        422: {"description": "Некорректный формат JSON"},
        500: {"description": "Внутренняя ошибка сервера"}
    }
)
async def extract_skills_from_text(text: str = Body(embed=True)):
    return ApiServices.analyze_text_for_skills(text)


@api_router.post(
    "/extract-from-file",
    response_model=SkillsResponse,
    summary="Извлечение навыков из файла",
    description="""Принимает файл (PDF или DOCX) с резюме и извлекает из него список навыков.
    Поддерживаются форматы: `.pdf`, `.docx`.""",
    responses={
        200: {
            "description": "Список найденных навыков из файла",
            "content": {
                "application/json": {
                    "example": {"skills": ["Python", "FastAPI", "SQLAlchemy"]}
                }
            }
        },
        400: {"description": "Файл не поддерживается или повреждён"},
        413: {"description": "Файл слишком большой"},
        500: {"description": "Внутренняя ошибка сервера"}
    }
)
async def extract_skills_from_file(file: UploadFile = File()) -> SkillsResponse:
    return await ApiServices.process_uploaded_file(file)