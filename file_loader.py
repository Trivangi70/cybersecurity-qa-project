# file_loader.py
import os
import PyPDF2

def load_file(filepath):
    """
    Reads and returns the text content from a PDF or TXT file.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None

    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == ".txt":
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()

        elif ext == ".pdf":
            text = ""
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text

        else:
            print(f"Unsupported file type: {ext}")
            return None

    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None
