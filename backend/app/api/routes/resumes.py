from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.schemas.match import ResumeMatchResponse
from app.schemas.resume import ResumeExtractResponse, ResumeParseResponse
from app.services.pdf_text_extractor import PdfParseError
from app.services.resume_cache import CacheLookup, CachedParsedResume, get_or_parse_resume
from app.services.resume_extraction_service import extract_resume_information
from app.services.resume_match_service import match_resume_file_text
from app.services.resume_text_cleaner import build_text_preview

router = APIRouter()


def _is_pdf_file(file: UploadFile) -> bool:
    filename = file.filename or ""
    return file.content_type == "application/pdf" or filename.lower().endswith(".pdf")


@router.post("/resumes/parse", response_model=ResumeParseResponse)
async def parse_resume(file: UploadFile = File(...)) -> ResumeParseResponse:
    parsed_lookup = await _read_and_parse_resume(file)
    parsed = parsed_lookup.value

    return ResumeParseResponse(
        filename=file.filename or "resume.pdf",
        resume_hash=parsed.resume_hash,
        page_count=parsed.page_count,
        raw_text=parsed.raw_text,
        cleaned_text_preview=build_text_preview(parsed.cleaned_text),
        raw_text_length=len(parsed.raw_text),
        cleaned_text_length=len(parsed.cleaned_text),
        cache_hit=parsed_lookup.hit,
    )


@router.post("/resumes/extract", response_model=ResumeExtractResponse)
async def extract_resume(file: UploadFile = File(...)) -> ResumeExtractResponse:
    parsed_lookup = await _read_and_parse_resume(file)
    parsed = parsed_lookup.value
    result = extract_resume_information(parsed.cleaned_text)

    return ResumeExtractResponse(
        filename=file.filename or "resume.pdf",
        resume_hash=parsed.resume_hash,
        page_count=parsed.page_count,
        data=result.data,
        cleaned_text_preview=build_text_preview(parsed.cleaned_text),
        extraction_method=result.method,
        warnings=result.warnings,
        cache_hit=parsed_lookup.hit,
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

    parsed_lookup = await _read_and_parse_resume(file)
    parsed = parsed_lookup.value
    return match_resume_file_text(
        filename=file.filename or "resume.pdf",
        resume_hash=parsed.resume_hash,
        page_count=parsed.page_count,
        cleaned_resume_text=parsed.cleaned_text,
        jd_text=jd_text,
        parse_cache_hit=parsed_lookup.hit,
    )


async def _read_and_parse_resume(file: UploadFile) -> CacheLookup[CachedParsedResume]:
    if not _is_pdf_file(file):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF files are supported.",
        )

    content = await file.read()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    try:
        return get_or_parse_resume(content)
    except PdfParseError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
