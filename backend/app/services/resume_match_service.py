from app.schemas.match import ResumeMatchResponse
from app.services.ai_match_scorer import AiMatchError, score_resume_match_with_ai
from app.services.hash_utils import hash_text
from app.services.resume_extraction_service import extract_resume_information
from app.services.resume_cache import build_match_cache_key, match_result_cache
from app.services.resume_text_cleaner import build_text_preview, clean_resume_text
from app.services.rule_jd_extractor import analyze_jd_text
from app.services.rule_match_scorer import score_resume_match


def match_resume_file_text(
    filename: str,
    resume_hash: str,
    page_count: int,
    cleaned_resume_text: str,
    jd_text: str,
    parse_cache_hit: bool = False,
) -> ResumeMatchResponse:
    cleaned_text = clean_resume_text(cleaned_resume_text)
    jd_hash = hash_text(jd_text)
    cache_key = build_match_cache_key(resume_hash, jd_hash)
    cached = match_result_cache.get(cache_key)
    if isinstance(cached, ResumeMatchResponse):
        return cached.model_copy(
            update={
                "filename": filename,
                "parse_cache_hit": parse_cache_hit,
                "match_cache_hit": True,
            }
        )

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

    response = ResumeMatchResponse(
        filename=filename,
        resume_hash=resume_hash,
        jd_hash=jd_hash,
        page_count=page_count,
        resume=resume_result.data,
        jd=jd_analysis,
        match=match_result,
        cleaned_text_preview=build_text_preview(cleaned_text),
        extraction_method=resume_result.method,
        warnings=warnings,
        parse_cache_hit=parse_cache_hit,
        match_cache_hit=False,
    )
    match_result_cache.set(cache_key, response)
    return response
