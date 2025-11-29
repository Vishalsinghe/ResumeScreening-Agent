# backend/parser.py
import io
from typing import BinaryIO
import PyPDF2

def extract_text_from_upload(uploaded_file: BinaryIO) -> str:
    """
    Accepts a Streamlit UploadedFile (file-like) and returns extracted text.
    Supports: PDF and TXT.
    """
    filename = getattr(uploaded_file, "name", "file").lower()
    uploaded_file.seek(0)
    if filename.endswith(".pdf"):
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return "\n\n".join(text_parts).strip()
        except Exception as e:
            # Fallback: read binary and try to decode (rare)
            uploaded_file.seek(0)
            raw = uploaded_file.read()
            try:
                return raw.decode("utf-8", errors="ignore")
            except Exception:
                raise RuntimeError(f"Could not parse PDF: {e}")
    else:
        # treat as text
        uploaded_file.seek(0)
        raw = uploaded_file.read()
        if isinstance(raw, bytes):
            return raw.decode("utf-8", errors="ignore")
        return str(raw)

