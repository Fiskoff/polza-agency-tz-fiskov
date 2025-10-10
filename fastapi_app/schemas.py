from pydantic import BaseModel, Field
from typing import List


class SkillsResponse(BaseModel):
    skills: List[str] = Field(
        description="Список найденных навыков",
        examples=[["Python", "FastAPI", "Docker"]]
    )