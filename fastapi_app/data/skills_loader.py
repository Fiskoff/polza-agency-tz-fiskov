import json
from pathlib import Path


def load_skills():
    file_path = Path(__file__).parent.parent / "data" / "skills.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["skills"]