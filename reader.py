# reader.py
import os
from PyPDF2 import PdfReader
from docx import Document

def read_file_content(path):
    ext = os.path.splitext(path)[1].lower()

    try:
        if ext == ".txt":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        elif ext == ".pdf":
            reader = PdfReader(path)
            text = []
            for page in reader.pages:
                text.append(page.extract_text() or "")
            return "\n".join(text)

        elif ext == ".docx":
            doc = Document(path)
            return "\n".join([p.text for p in doc.paragraphs])

    except Exception as e:
        print(f"[Read Error] {path}: {e}")

    return ""  # Return empty if unsupported or error
