from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.schemas.match import ResumeMatchResponse
from app.schemas.resume import ResumeExtractResponse, ResumeParseResponse
from app.services.pdf_text_extractor import PdfParseError, PdfTextExtraction, extract_text_from_pdf
from app.services.resume_extraction_service import extract_resume_information
from app.services.resume_match_service import match_resume_file_text
from app.services.resume_text_cleaner import build_text_preview, clean_resume_text

router = APIRouter()


def _is_pdf_file(file: UploadFile) -> bool:
    filename = file.filename or ""
    return file.content_type == "application/pdf" or filename.lower().endswith(".pdf")


@router.post("/resumes/parse", response_model=ResumeParseResponse)
async def parse_resume(file: UploadFile = File(...)) -> ResumeParseResponse:
    extraction = await _read_and_extract_text(file)
    cleaned_text = clean_resume_text(extraction.raw_text)

    return ResumeParseResponse(
        filename=file.filename or "resume.pdf",
        page_count=extraction.page_count,
        raw_text=extraction.raw_text,
        cleaned_text_preview=build_text_preview(cleaned_text),
        raw_text_length=len(extraction.raw_text),
        cleaned_text_length=len(cleaned_text),
    )


@router.post("/resumes/extract", response_model=ResumeExtractResponse)
async def extract_resume(file: UploadFile = File(...)) -> ResumeExtractResponse:
    extraction = await _read_and_extract_text(file)
    cleaned_text = clean_resume_text(extraction.raw_text)
    result = extract_resume_information(cleaned_text)

    return ResumeExtractResponse(
        filename=file.filename or "resume.pdf",
        page_count=extraction.page_count,
        data=result.data,
        cleaned_text_preview=build_text_preview(cleaned_text),
        extraction_method=result.method,
        warnings=result.warnings,
    )


@router.post("/resumes/match", response_model=ResumeMatchResponse)
async def match_resume_with_jd(
    file: UploadFile = File(...),
    jd_text: str = Form(...),
) -> ResumeMatchResponse:
    if not jd_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JD text is required.",
        )

    extraction = await _read_and_extract_text(file)
    return match_resume_file_text(
        filename=file.filename or "resume.pdf",
        page_count=extraction.page_count,
        raw_resume_text=extraction.raw_text,
        jd_text=jd_text,
    )


async def _read_and_extract_text(file: UploadFile) -> PdfTextExtraction:
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
        return extract_text_from_pdf(content)
    except PdfParseError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
