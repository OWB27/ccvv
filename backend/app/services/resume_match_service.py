from app.schemas.match import ResumeMatchResponse
from app.services.ai_match_scorer import AiMatchError, score_resume_match_with_ai
from app.services.resume_extraction_service import extract_resume_information
from app.services.resume_text_cleaner import build_text_preview, clean_resume_text
from app.services.rule_jd_extractor import analyze_jd_text
from app.services.rule_match_scorer import score_resume_match


def match_resume_file_text(
    filename: str,
    page_count: int,
    raw_resume_text: str,
    jd_text: str,
) -> ResumeMatchResponse:
    cleaned_text = clean_resume_text(raw_resume_text)
    resume_result = extract_resume_information(cleaned_text)
    jd_analysis = analyze_jd_text(jd_text)
    warnings = list(resume_result.warnings)

    try:
        ai_result = score_resume_match_with_ai(
            resume=resume_result.data,
            jd=jd_analysis,
            jd_text=jd_text,
        )
        match_result = ai_result.match
        warnings.extend(ai_result.warnings)
    except AiMatchError as exc:
        warnings.append(str(exc))
        match_result = score_resume_match(
            resume=resume_result.data,
            jd=jd_analysis,
            resume_text=cleaned_text,
        )

    return ResumeMatchResponse(
        filename=filename,
        page_count=page_count,
        resume=resume_result.data,
        jd=jd_analysis,
        match=match_result,
        cleaned_text_preview=build_text_preview(cleaned_text),
        extraction_method=resume_result.method,
        warnings=warnings,
    )
