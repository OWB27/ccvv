import re

from app.schemas.match import JobDescriptionAnalysis
from app.services.jd_keywords import (
    EDUCATION_LEVELS,
    JD_SIGNAL_KEYWORDS,
    SKILL_KEYWORDS,
)


def analyze_jd_text(jd_text: str) -> JobDescriptionAnalysis:
    normalized = jd_text.strip()
    skills = _extract_skills(normalized)
    education = _extract_required_education(normalized)
    experience_years = _extract_required_experience(normalized)
    requirements = _extract_core_requirements(normalized)

    keywords = _dedupe(
        skills
        + _extract_signal_keywords(normalized)
        + _build_requirement_keywords(education, experience_years)
    )

    return JobDescriptionAnalysis(
        keywords=keywords[:20],
        required_skills=skills,
        required_education=education,
        required_experience_years=experience_years,
        core_requirements=requirements,
    )


def _extract_skills(text: str) -> list[str]:
    skills = []
    for skill in SKILL_KEYWORDS:
        if _contains_keyword(text, skill):
            skills.append(skill)
    return _dedupe(skills)


def _contains_keyword(text: str, keyword: str) -> bool:
    if re.search(r"[\u4e00-\u9fff]", keyword):
        return keyword in text

    pattern = rf"(?<![A-Za-z0-9]){re.escape(keyword)}(?![A-Za-z0-9])"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _extract_required_education(text: str) -> str | None:
    for education, _rank in EDUCATION_LEVELS:
        if education in text:
            return education
    return None


def _extract_required_experience(text: str) -> int | None:
    patterns = (
        r"(\d+)\s*年(?:以上)?(?:工作)?经验",
        r"(\d+)\s*\+\s*年(?:工作)?经验",
        r"经验\s*(\d+)\s*年",
    )
    years = []
    for pattern in patterns:
        years.extend(int(match) for match in re.findall(pattern, text))
    return min(years) if years else None


def _extract_core_requirements(text: str) -> list[str]:
    lines = [line.strip(" -*\t") for line in text.splitlines() if line.strip()]
    requirement_markers = ("要求", "职责", "任职", "负责", "熟悉", "掌握", "具备", "优先")
    requirements = [
        line for line in lines if any(marker in line for marker in requirement_markers)
    ]
    return requirements[:8]


def _extract_signal_keywords(text: str) -> list[str]:
    return [keyword for keyword in JD_SIGNAL_KEYWORDS if _contains_keyword(text, keyword)]


def _build_requirement_keywords(
    education: str | None,
    experience_years: int | None,
) -> list[str]:
    keywords = []
    if education:
        keywords.append(education)
    if experience_years is not None:
        keywords.append(f"{experience_years}年经验")
    return keywords


def _dedupe(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result
