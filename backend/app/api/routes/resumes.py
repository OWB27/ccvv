from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas.resume import ResumeParseResponse
from app.services.pdf_parser import PdfParseError, extract_text_from_pdf
from app.services.text_cleaner import build_text_preview, clean_resume_text

router = APIRouter()


def _is_pdf_file(file: UploadFile) -> bool:
    filename = file.filename or ""
    return file.content_type == "application/pdf" or filename.lower().endswith(".pdf")


@router.post("/resumes/parse", response_model=ResumeParseResponse)
async def parse_resume(file: UploadFile = File(...)) -> ResumeParseResponse:
    if not _is_pdf_file(file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    content = await file.read()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    try:
        extraction = extract_text_from_pdf(content)
    except PdfParseError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    cleaned_text = clean_resume_text(extraction.raw_text)

    return ResumeParseResponse(
        filename=file.filename or "resume.pdf",
        page_count=extraction.page_count,
        raw_text=extraction.raw_text,
        cleaned_text_preview=build_text_preview(cleaned_text),
        raw_text_length=len(extraction.raw_text),
        cleaned_text_length=len(cleaned_text),
    )

