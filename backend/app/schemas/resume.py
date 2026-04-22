from pydantic import BaseModel


class ResumeParseResponse(BaseModel):
    filename: str
    page_count: int
    raw_text: str
    cleaned_text_preview: str
    raw_text_length: int
    cleaned_text_length: int

