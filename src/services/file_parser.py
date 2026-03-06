import os
from pathlib import Path
from pypdf import PdfReader
from docx import Document


class FileParser:

    @staticmethod
    async def parse_pdf(file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            return f"Ошибка при чтении PDF: {e}"

    @staticmethod
    async def parse_docx(file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            return f"Ошибка при чтении DOCX: {e}"

    @staticmethod
    async def parse_txt(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            return f"Ошибка при чтении TXT: {e}"

    @staticmethod
    async def parse_file(file_path: str, file_type: str) -> str:
        if file_type == 'application/pdf':
            return await FileParser.parse_pdf(file_path)
        elif file_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                           'application/msword']:
            return await FileParser.parse_docx(file_path)
        elif file_type == 'text/plain':
            return await FileParser.parse_txt(file_path)
        else:
            return "Неподдерживаемый тип файла"