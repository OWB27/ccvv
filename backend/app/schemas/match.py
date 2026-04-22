from pydantic import BaseModel, Field

from app.schemas.resume import ResumeStructuredData


class JobDescriptionAnalyzeRequest(BaseModel):
    jd_text: str


class JobDescriptionAnalysis(BaseModel):
    keywords: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)
    required_education: str | None = None
    required_experience_years: int | None = None
    core_requirements: list[str] = Field(default_factory=list)


class ScoreBreakdown(BaseModel):
    skill_score: int
    education_score: int
    experience_score: int
    project_score: int


class MatchResult(BaseModel):
    score: int
    summary: str
    explanations: list[str] = Field(default_factory=list)
    matched_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    breakdown: ScoreBreakdown


class JobDescriptionAnalyzeResponse(BaseModel):
    jd: JobDescriptionAnalysis


class ResumeMatchResponse(BaseModel):
    filename: str
    page_count: int
    resume: ResumeStructuredData
    jd: JobDescriptionAnalysis
    match: MatchResult
    cleaned_text_preview: str
    extraction_method: str
    warnings: list[str] = Field(default_factory=list)

