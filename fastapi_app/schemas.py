from pydantic import BaseModel
from typing import List


class ResumeResponse(BaseModel):
    skills: List[str]