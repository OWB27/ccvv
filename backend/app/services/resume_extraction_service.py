from dataclasses import dataclass

from app.core.config import settings
from app.schemas.resume import ResumeStructuredData
from app.services.ai_resume_extractor import (
    AiResumeExtractionError,
    extract_resume_with_ai,
)
from app.services.rule_resume_extractor import extract_resume_with_rules


@dataclass(frozen=True)
class ResumeExtractionResult:
    data: ResumeStructuredData
    method: str
    warnings: list[str]


def extract_resume_information(cleaned_text: str) -> ResumeExtractionResult:
    warnings: list[str] = []

    if not cleaned_text.strip():
        return ResumeExtractionResult(
            data=ResumeStructuredData(),
            method="fallback",
            warnings=["Cleaned resume text is empty."],
        )

    if settings.AI_API_KEY:
        try:
            return ResumeExtractionResult(
                data=extract_resume_with_ai(cleaned_text),
                method="ai",
                warnings=[],
            )
        except AiResumeExtractionError as exc:
            warnings.append(str(exc))

    fallback_data = extract_resume_with_rules(cleaned_text)
    if not settings.AI_API_KEY:
        warnings.append("AI_API_KEY or OPENAI_API_KEY is not configured; used rule-based fallback.")

    return ResumeExtractionResult(
        data=fallback_data,
        method="fallback",
        warnings=warnings,
    )
