import re

from app.schemas.match import JobDescriptionAnalysis


SKILL_KEYWORDS = (
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "Go",
    "C++",
    "FastAPI",
    "Django",
    "Flask",
    "Spring",
    "React",
    "Vue",
    "Node.js",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "Redis",
    "MongoDB",
    "Docker",
    "Kubernetes",
    "Linux",
    "Git",
    "REST",
    "API",
    "LLM",
    "NLP",
    "PyTorch",
    "TensorFlow",
    "机器学习",
    "深度学习",
    "数据分析",
    "微服务",
    "后端",
    "前端",
    "算法",
)

EDUCATION_LEVELS = (
    ("博士", 4),
    ("硕士", 3),
    ("研究生", 3),
    ("本科", 2),
    ("学士", 2),
    ("大专", 1),
    ("专科", 1),
)


def analyze_jd_text(jd_text: str) -> JobDescriptionAnalysis:
    normalized = jd_text.strip()
    skills = _extract_skills(normalized)
    education = _extract_required_education(normalized)
    experience_years = _extract_required_experience(normalized)
    requirements = _extract_core_requirements(normalized)

    keywords = _dedupe(skills + _extract_chinese_keywords(normalized))

    return JobDescriptionAnalysis(
        keywords=keywords[:30],
        required_skills=skills,
        required_education=education,
        required_experience_years=experience_years,
        core_requirements=requirements,
    )


def _extract_skills(text: str) -> list[str]:
    lower_text = text.lower()
    skills = []
    for skill in SKILL_KEYWORDS:
        if skill.lower() in lower_text:
            skills.append(skill)
    return _dedupe(skills)


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


def _extract_chinese_keywords(text: str) -> list[str]:
    candidates = re.findall(r"[\u4e00-\u9fffA-Za-z0-9.+#-]{2,}", text)
    stop_words = {"岗位职责", "任职要求", "以上", "负责", "熟悉", "掌握", "具备", "优先"}
    keywords = []
    for candidate in candidates:
        if candidate in stop_words or candidate.isdigit():
            continue
        if len(candidate) > 24:
            continue
        keywords.append(candidate)
    return _dedupe(keywords)


def _dedupe(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result

