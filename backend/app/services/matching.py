import re

from app.schemas.match import JobDescriptionAnalysis, MatchResult, ScoreBreakdown
from app.schemas.resume import ResumeStructuredData


EDUCATION_RANKS = {
    "专科": 1,
    "大专": 1,
    "本科": 2,
    "学士": 2,
    "硕士": 3,
    "研究生": 3,
    "博士": 4,
}


def score_resume_match(
    resume: ResumeStructuredData,
    jd: JobDescriptionAnalysis,
    resume_text: str,
) -> MatchResult:
    resume_corpus = _build_resume_corpus(resume, resume_text)
    matched_keywords, missing_keywords = _match_keywords(jd.required_skills, resume_corpus)

    skill_score = _score_skills(jd.required_skills, matched_keywords)
    education_score = _score_education(resume, jd)
    experience_score = _score_experience(resume, jd, resume_corpus)
    project_score = _score_projects(resume, jd, resume_corpus)

    total = skill_score + education_score + experience_score + project_score
    explanations = _build_explanations(
        jd=jd,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        skill_score=skill_score,
        education_score=education_score,
        experience_score=experience_score,
        project_score=project_score,
    )

    return MatchResult(
        score=min(100, max(0, total)),
        summary=_build_summary(total),
        explanations=explanations,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        breakdown=ScoreBreakdown(
            skill_score=skill_score,
            education_score=education_score,
            experience_score=experience_score,
            project_score=project_score,
        ),
    )


def _score_skills(required_skills: list[str], matched_keywords: list[str]) -> int:
    if not required_skills:
        return 35
    return round(45 * len(matched_keywords) / len(required_skills))


def _score_education(resume: ResumeStructuredData, jd: JobDescriptionAnalysis) -> int:
    if not jd.required_education:
        return 12

    required_rank = EDUCATION_RANKS.get(jd.required_education, 0)
    resume_rank = 0
    for item in resume.education:
        text = " ".join(
            value for value in [item.school, item.degree, item.major, item.period] if value
        )
        for education, rank in EDUCATION_RANKS.items():
            if education in text:
                resume_rank = max(resume_rank, rank)

    if resume_rank >= required_rank and required_rank > 0:
        return 15
    if resume_rank > 0:
        return 8
    return 4


def _score_experience(
    resume: ResumeStructuredData,
    jd: JobDescriptionAnalysis,
    resume_corpus: str,
) -> int:
    resume_years = _extract_resume_years(resume, resume_corpus)
    has_work = bool(resume.work_experience)

    if jd.required_experience_years is None:
        return 20 if has_work or resume_years else 14
    if resume_years >= jd.required_experience_years:
        return 25
    if has_work:
        return 14
    return 6


def _score_projects(
    resume: ResumeStructuredData,
    jd: JobDescriptionAnalysis,
    resume_corpus: str,
) -> int:
    if not resume.projects:
        return 4

    project_text = " ".join(
        " ".join(
            value
            for value in [
                project.name,
                project.role,
                project.description,
                " ".join(project.highlights),
                " ".join(project.technologies),
            ]
            if value
        )
        for project in resume.projects
    ).lower()

    matched = [
        keyword for keyword in jd.keywords[:20] if keyword.lower() in project_text or keyword.lower() in resume_corpus
    ]
    if matched:
        return 15
    return 9


def _match_keywords(required_skills: list[str], resume_corpus: str) -> tuple[list[str], list[str]]:
    matched = []
    missing = []
    lower_corpus = resume_corpus.lower()
    for skill in required_skills:
        if skill.lower() in lower_corpus:
            matched.append(skill)
        else:
            missing.append(skill)
    return matched, missing


def _build_resume_corpus(resume: ResumeStructuredData, resume_text: str) -> str:
    parts = [
        resume_text,
        resume.job_intention or "",
        resume.years_of_experience or "",
    ]
    for item in resume.education:
        parts.extend([item.school or "", item.degree or "", item.major or ""])
    for item in resume.work_experience:
        parts.extend(
            [
                item.company or "",
                item.position or "",
                item.description or "",
                " ".join(item.highlights),
                " ".join(item.technologies),
            ]
        )
    for item in resume.projects:
        parts.extend(
            [
                item.name or "",
                item.role or "",
                item.description or "",
                " ".join(item.highlights),
                " ".join(item.technologies),
            ]
        )
    return " ".join(parts).lower()


def _extract_resume_years(resume: ResumeStructuredData, resume_corpus: str) -> int:
    candidates = []
    if resume.years_of_experience:
        candidates.extend(int(item) for item in re.findall(r"\d+", resume.years_of_experience))
    candidates.extend(int(item) for item in re.findall(r"(\d+)\s*年(?:以上)?(?:工作)?经验", resume_corpus))
    return max(candidates) if candidates else 0


def _build_explanations(
    jd: JobDescriptionAnalysis,
    matched_keywords: list[str],
    missing_keywords: list[str],
    skill_score: int,
    education_score: int,
    experience_score: int,
    project_score: int,
) -> list[str]:
    explanations = [
        f"技能匹配得分 {skill_score}/45，命中 {len(matched_keywords)} 个核心技能。",
        f"学历相关性得分 {education_score}/15。",
        f"工作经验相关性得分 {experience_score}/25。",
        f"项目经历相关性得分 {project_score}/15。",
    ]
    if jd.required_experience_years is not None:
        explanations.append(f"JD 要求约 {jd.required_experience_years} 年经验。")
    if missing_keywords:
        explanations.append(f"待补充或未识别技能：{', '.join(missing_keywords[:8])}。")
    return explanations


def _build_summary(score: int) -> str:
    if score >= 85:
        return "匹配度高，简历与岗位要求高度一致。"
    if score >= 70:
        return "匹配度较好，核心要求有一定覆盖。"
    if score >= 50:
        return "匹配度中等，存在若干关键差距。"
    return "匹配度偏低，需要补充更多与 JD 相关的经历和技能。"

