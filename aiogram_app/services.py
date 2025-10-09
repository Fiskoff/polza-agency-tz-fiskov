import fitz
import docx


class BotService:
    @staticmethod
    def extract_text_from_file(file_name: str) -> str:
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