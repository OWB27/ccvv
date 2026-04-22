from pydantic import BaseModel, Field


class ResumeParseResponse(BaseModel):
    filename: str
    page_count: int
    raw_text: str
    cleaned_text_preview: str
    raw_text_length: int
    cleaned_text_length: int


class EducationItem(BaseModel):
    school: str | None = None
    degree: str | None = None
    major: str | None = None
    period: str | None = None


class ProjectItem(BaseModel):
    name: str | None = None
    role: str | None = None
    description: str | None = None
    highlights: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)


class ResumeStructuredData(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    job_intention: str | None = None
    expected_salary: str | None = None
    years_of_experience: str | None = None
    education: list[EducationItem] = Field(default_factory=list)
    projects: list[ProjectItem] = Field(default_factory=list)


class ResumeExtractResponse(BaseModel):
    filename: str
    page_count: int
    data: ResumeStructuredData
    cleaned_text_preview: str
    extraction_method: str
    warnings: list[str] = Field(default_factory=list)
