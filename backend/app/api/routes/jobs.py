from fastapi import APIRouter, HTTPException, status

from app.schemas.match import JobDescriptionAnalyzeRequest, JobDescriptionAnalyzeResponse
from app.services.rule_jd_extractor import analyze_jd_text

router = APIRouter()


@router.post("/jobs/analyze", response_model=JobDescriptionAnalyzeResponse)
def analyze_job_description(
    payload: JobDescriptionAnalyzeRequest,
) -> JobDescriptionAnalyzeResponse:
    if not payload.jd_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JD text is required.",
        )

    return JobDescriptionAnalyzeResponse(jd=analyze_jd_text(payload.jd_text))
