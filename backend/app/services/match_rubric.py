from dataclasses import dataclass


@dataclass(frozen=True)
class MatchRubric:
    skill_score: int = 45
    education_score: int = 15
    experience_score: int = 25
    project_score: int = 15

    @property
    def total_score(self) -> int:
        return (
            self.skill_score
            + self.education_score
            + self.experience_score
            + self.project_score
        )


MATCH_RUBRIC = MatchRubric()


def match_rubric_schema() -> dict[str, object]:
    return {
        "score": f"integer from 0 to {MATCH_RUBRIC.total_score}",
        "summary": "short Chinese summary",
        "explanations": ["Chinese explanation string"],
        "matched_keywords": ["string"],
        "missing_keywords": ["string"],
        "breakdown": {
            "skill_score": f"integer from 0 to {MATCH_RUBRIC.skill_score}",
            "education_score": f"integer from 0 to {MATCH_RUBRIC.education_score}",
            "experience_score": f"integer from 0 to {MATCH_RUBRIC.experience_score}",
            "project_score": f"integer from 0 to {MATCH_RUBRIC.project_score}",
        },
    }
