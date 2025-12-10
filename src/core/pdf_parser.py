import io
import pdfplumber

def parse_pdf_bytes(data: bytes) -> str:
    text = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text)
