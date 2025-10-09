import re

import fitz
import docx

from fastapi_app.data.skills_loader import load_skills


class ApiServices:
    @staticmethod
    def extract_skills_from_text(text: str) -> set:
        skill_patterns = load_skills()
        found_skills = set()

        for skill, pattern in skill_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.add(skill)

        return found_skills

    @staticmethod
    def extract_text_from_file(file_path: str) -> str:
        text = ""
        if file_path.endswith('.pdf'):
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        elif file_path.endswith('.docx'):
            doc = docx.Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
        return text
