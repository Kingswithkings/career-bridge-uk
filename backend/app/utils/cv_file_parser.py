from io import BytesIO
from pathlib import Path
from zipfile import BadZipFile

from fastapi import HTTPException, UploadFile

SUPPORTED_CV_EXTENSIONS = {".txt", ".md", ".markdown", ".rtf", ".docx", ".pdf"}


async def extract_cv_text(file: UploadFile) -> str:
    filename = file.filename or ""
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_CV_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Upload a CV as PDF, DOCX, TXT, MD, Markdown, or RTF.",
        )

    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="The uploaded CV file is empty.")

    if extension in {".txt", ".md", ".markdown", ".rtf"}:
        text = content.decode("utf-8", errors="ignore")
    elif extension == ".docx":
        text = extract_docx_text(content)
    else:
        text = extract_pdf_text(content)

    text = text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract readable text from that CV. Try another file or paste the CV text.",
        )

    return text


def extract_docx_text(content: bytes) -> str:
    try:
        from docx import Document

        document = Document(BytesIO(content))
    except BadZipFile as exc:
        raise HTTPException(status_code=400, detail="That DOCX file could not be read.") from exc

    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def extract_pdf_text(content: bytes) -> str:
    try:
        from pypdf import PdfReader

        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="That PDF file could not be read.") from exc
