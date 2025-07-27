import os
from PIL import Image
import pytesseract  # OCR

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"]

def read_file_content(path):
    ext = os.path.splitext(path)[1].lower()

    try:
        if ext == ".txt":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        elif ext == ".pdf":
            from PyPDF2 import PdfReader
            reader = PdfReader(path)
            return "\n".join([page.extract_text() or "" for page in reader.pages])

        elif ext == ".docx":
            from docx import Document
            doc = Document(path)
            return "\n".join([p.text for p in doc.paragraphs])

        elif ext in IMAGE_EXTENSIONS:
            image = Image.open(path)
            text = pytesseract.image_to_string(image)  # OCR
            return f"[Image: {os.path.basename(path)}]\n{text.strip()}"

    except Exception as e:
        print(f"[Read Error] {path}: {e}")

    return ""
