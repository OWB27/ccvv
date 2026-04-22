import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from app.core.config import settings
from app.schemas.match import JobDescriptionAnalysis, MatchResult, ScoreBreakdown
from app.schemas.resume import ResumeStructuredData


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
    if not settings.AI_API_KEY:
        raise AiMatchError("AI_API_KEY or OPENAI_API_KEY is not configured; used rule-based score.")

    payload = {
        "model": settings.AI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You score resume-to-JD matching. Return strict JSON only.",
            },
            {
                "role": "user",
                "content": _build_prompt(resume, jd, jd_text),
            },
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    request = urllib.request.Request(
        url=f"{settings.AI_BASE_URL.rstrip('/')}/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.AI_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
        content = response_payload["choices"][0]["message"]["content"]
        data = json.loads(content)
        return AiMatchResult(match=_validate_ai_match(data), warnings=[])
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, IndexError, TypeError, ValueError) as exc:
        raise AiMatchError("LLM match scoring failed; used rule-based score.") from exc


def _build_prompt(resume: ResumeStructuredData, jd: JobDescriptionAnalysis, jd_text: str) -> str:
    schema = {
        "score": "integer from 0 to 100",
        "summary": "short Chinese summary",
        "explanations": ["Chinese explanation string"],
        "matched_keywords": ["string"],
        "missing_keywords": ["string"],
        "breakdown": {
            "skill_score": "integer from 0 to 45",
            "education_score": "integer from 0 to 15",
            "experience_score": "integer from 0 to 25",
            "project_score": "integer from 0 to 15",
        },
    }
    return (
        "Score how well the structured resume matches the JD. Use a transparent 100-point rubric: "
        "skills 45, education 15, work experience 25, projects 15. Do not invent facts. "
        "If a candidate has no work or project experience, the corresponding score is 0."
        "As a professional HR specialist and software engineer, scoring must be rigorous and objective to align with today's highly competitive job market."
        "Return JSON exactly matching this schema:\n"
        f"{json.dumps(schema, ensure_ascii=False)}\n\n"
        "Structured resume:\n"
        f"{resume.model_dump_json(exclude_none=True)}\n\n"
        "JD analysis:\n"
        f"{jd.model_dump_json(exclude_none=True)}\n\n"
        "Original JD text:\n"
        f"{jd_text[:8000]}"
    )


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
            skill_score=_clamp_int(breakdown.get("skill_score"), 0, 45),
            education_score=_clamp_int(breakdown.get("education_score"), 0, 15),
            experience_score=_clamp_int(breakdown.get("experience_score"), 0, 25),
            project_score=_clamp_int(breakdown.get("project_score"), 0, 15),
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

