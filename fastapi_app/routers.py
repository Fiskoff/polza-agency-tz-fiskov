import os
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException

from fastapi_app.schemas import ResumeResponse
from fastapi_app.services import ApiServices


api_router = APIRouter()

@api_router.post("/analyze", response_model=ResumeResponse)
async def analyze_resume(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Файл должен быть PDF или DOCX")

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        text = ApiServices.extract_text_from_file(temp_path)
        found_skills = ApiServices.extract_skills_from_text(text)
        return ResumeResponse(skills=list(found_skills))
    finally:
        os.remove(temp_path)