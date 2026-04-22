from typing import Any

from app.schemas.resume import ResumeStructuredData
from app.services.ai_client import AiClientError, request_json_object
from app.services.ai_prompts import (
    RESUME_EXTRACTION_SYSTEM_PROMPT,
    build_resume_extraction_prompt,
)


class AiResumeExtractionError(Exception):
    """Raised when AI resume extraction cannot produce valid structured data."""


def extract_resume_with_ai(cleaned_text: str) -> ResumeStructuredData:
    try:
        data = request_json_object(
            system_prompt=RESUME_EXTRACTION_SYSTEM_PROMPT,
            user_prompt=build_resume_extraction_prompt(cleaned_text),
        )
        return _validate_structured_data(data)
    except (AiClientError, ValueError) as exc:
        raise AiResumeExtractionError(f"{exc} Used rule-based fallback.") from exc


def _validate_structured_data(data: dict[str, Any]) -> ResumeStructuredData:
    data = _normalize_null_strings(data)
    data.setdefault("education", [])
    data.setdefault("work_experience", [])
    data.setdefault("projects", [])
    return ResumeStructuredData(**data)


def _normalize_null_strings(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalize_null_strings(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_null_strings(item) for item in value]
    if isinstance(value, str) and value.strip().lower() in {"null", "none", "n/a"}:
        return None
    return value
