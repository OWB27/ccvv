import json

from app.schemas.match import JobDescriptionAnalysis
from app.schemas.resume import ResumeStructuredData
from app.services.match_rubric import MATCH_RUBRIC, match_rubric_schema


RESUME_EXTRACTION_SYSTEM_PROMPT = (
    "You extract resume information and return strict JSON only."
)

MATCH_SCORING_SYSTEM_PROMPT = (
    "You score resume-to-JD matching. Return strict JSON only."
)

RESUME_SCHEMA_INSTRUCTION = {
    "name": "string or null",
    "phone": "string or null",
    "email": "string or null",
    "address": "string or null",
    "job_intention": "string or null",
    "expected_salary": "string or null",
    "years_of_experience": "string or null",
    "education": [
        {
            "school": "string or null",
            "degree": "string or null",
            "major": "string or null",
            "period": "string or null",
        }
    ],
    "work_experience": [
        {
            "company": "string or null",
            "position": "string or null",
            "period": "string or null",
            "description": "string or null, one-sentence work summary",
            "highlights": ["string"],
            "technologies": ["string"],
        }
    ],
    "projects": [
        {
            "name": "string or null",
            "role": "string or null",
            "description": "string or null, one-sentence project summary",
            "highlights": ["string"],
            "technologies": ["string"],
        }
    ],
}


def build_resume_extraction_prompt(cleaned_text: str) -> str:
    clipped_text = cleaned_text[:20000]
    return (
        "Extract resume information as strict JSON only. Use only the resume text; do not invent facts. "
        "Use JSON null or [] when unknown. For projects, put the short summary in description, "
        "and put bullet points/responsibilities/achievements/metrics in highlights. "
        "For work_experience, extract company, position, period, summary, responsibilities, achievements, "
        "metrics, and technologies that can help later JD matching.\n\n"
        "Schema:\n"
        f"{json.dumps(RESUME_SCHEMA_INSTRUCTION, ensure_ascii=False)}\n\n"
        "Resume text:\n"
        f"{clipped_text}"
    )


def build_match_scoring_prompt(
    resume: ResumeStructuredData,
    jd: JobDescriptionAnalysis,
    jd_text: str,
) -> str:
    return (
        "Score how well the structured resume matches the JD. Use this 100-point rubric: "
        f"skills {MATCH_RUBRIC.skill_score}, education {MATCH_RUBRIC.education_score}, "
        f"work experience {MATCH_RUBRIC.experience_score}, projects {MATCH_RUBRIC.project_score}. "
        "Do not invent facts. If a candidate has no work or project experience, that score is 0. "
        "As a professional HR specialist and software engineer, scoring must be rigorous and objective. "
        "Return JSON exactly matching this schema:\n"
        f"{json.dumps(match_rubric_schema(), ensure_ascii=False)}\n\n"
        "Structured resume:\n"
        f"{resume.model_dump_json(exclude_none=True)}\n\n"
        "JD analysis:\n"
        f"{jd.model_dump_json(exclude_none=True)}\n\n"
        "Original JD text:\n"
        f"{jd_text[:8000]}"
    )
