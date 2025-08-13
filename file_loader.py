import os
import PyPDF2

def load_file(file_path):
    """Load content from a text or PDF file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    _, ext = os.path.splitext(file_path)

    if ext.lower() == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext.lower() == ".pdf":
        text = ""
        with open(file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        return text

    else:
        raise ValueError(f"Unsupported file type: {ext}")

