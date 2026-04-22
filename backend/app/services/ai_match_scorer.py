from dataclasses import dataclass
from typing import Any

from app.schemas.match import JobDescriptionAnalysis, MatchResult, ScoreBreakdown
from app.schemas.resume import ResumeStructuredData
from app.services.ai_client import AiClientError, request_json_object
from app.services.ai_prompts import (
    MATCH_SCORING_SYSTEM_PROMPT,
    build_match_scoring_prompt,
)
from app.services.match_rubric import MATCH_RUBRIC


class AiMatchError(Exception):
    """Raised when LLM matching cannot produce a valid score."""


@dataclass(frozen=True)
class AiMatchResult:
    match: MatchResult
    warnings: list[str]


def score_resume_match_with_ai(
    resume: ResumeStructuredData,
    jd: JobDescriptionAnalysis,
    jd_text: str,
) -> AiMatchResult:
    try:
        data = request_json_object(
            system_prompt=MATCH_SCORING_SYSTEM_PROMPT,
            user_prompt=build_match_scoring_prompt(resume, jd, jd_text),
        )
        return AiMatchResult(match=_validate_ai_match(data), warnings=[])
    except (AiClientError, ValueError) as exc:
        raise AiMatchError(f"{exc} Used rule-based score.") from exc


def _validate_ai_match(data: dict[str, Any]) -> MatchResult:
    if not isinstance(data, dict):
        raise ValueError("AI match output is not a JSON object")

    breakdown = data.get("breakdown") or {}
    score = _clamp_int(data.get("score"), 0, 100)
    match = MatchResult(
        score=score,
        summary=str(data.get("summary") or _fallback_summary(score)),
        scoring_method="ai",
        explanations=_string_list(data.get("explanations")),
        matched_keywords=_string_list(data.get("matched_keywords")),
        missing_keywords=_string_list(data.get("missing_keywords")),
        breakdown=ScoreBreakdown(
            skill_score=_clamp_int(breakdown.get("skill_score"), 0, MATCH_RUBRIC.skill_score),
            education_score=_clamp_int(
                breakdown.get("education_score"),
                0,
                MATCH_RUBRIC.education_score,
            ),
            experience_score=_clamp_int(
                breakdown.get("experience_score"),
                0,
                MATCH_RUBRIC.experience_score,
            ),
            project_score=_clamp_int(breakdown.get("project_score"), 0, MATCH_RUBRIC.project_score),
        ),
    )

    return match


def _clamp_int(value: Any, minimum: int, maximum: int) -> int:
    try:
        number = int(round(float(value)))
    except (TypeError, ValueError):
        number = minimum
    return min(maximum, max(minimum, number))


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None]


def _fallback_summary(score: int) -> str:
    if score >= 85:
        return "匹配度高，简历与岗位要求高度一致。"
    if score >= 70:
        return "匹配度较好，核心要求有一定覆盖。"
    if score >= 50:
        return "匹配度中等，存在若干关键差距。"
    return "匹配度偏低，需要补充更多与 JD 相关的经历和技能。"
