from app.schemas.match import JobDescriptionAnalysis
from app.schemas.resume import EducationItem, ProjectItem, ResumeStructuredData, WorkExperienceItem
from app.services.rule_match_scorer import score_resume_match


def test_rule_match_score_explains_core_dimensions():
    resume = ResumeStructuredData(
        name="张三",
        years_of_experience="3年工作经验",
        education=[EducationItem(school="某某大学", degree="本科", major="计算机科学")],
        work_experience=[
            WorkExperienceItem(
                company="某某科技有限公司",
                position="Python 后端工程师",
                description="负责 FastAPI 服务和 SQL 数据建模",
                technologies=["Python", "FastAPI", "SQL"],
            )
        ],
        projects=[
            ProjectItem(
                name="智能简历分析系统",
                description="基于 Python 和 FastAPI 的简历分析平台",
                technologies=["Python", "FastAPI"],
            )
        ],
    )
    jd = JobDescriptionAnalysis(
        keywords=["Python", "FastAPI", "SQL", "本科", "3年经验"],
        required_skills=["Python", "FastAPI", "SQL"],
        required_education="本科",
        required_experience_years=3,
    )

    result = score_resume_match(
        resume=resume,
        jd=jd,
        resume_text="Python FastAPI SQL 3年工作经验 本科 项目经历",
    )

    assert result.scoring_method == "rule"
    assert result.score >= 85
    assert result.breakdown.skill_score > 0
    assert "Python" in result.matched_keywords
    assert result.explanations

