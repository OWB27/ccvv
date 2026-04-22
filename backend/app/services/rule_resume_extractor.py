import re
from typing import Any

from app.schemas.resume import ResumeStructuredData


def extract_resume_with_rules(text: str) -> ResumeStructuredData:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    email = _find_first(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", text)
    phone = _find_first(r"(?:\+?\d{1,3}[- ]?)?(?:1[3-9]\d{9}|\d{3,4}[- ]?\d{7,8})", text)

    return ResumeStructuredData(
        name=_guess_name(lines),
        phone=phone,
        email=email,
        address=_find_labeled_value(lines, ["地址", "现居地", "所在地", "Address"]),
        job_intention=_find_labeled_value(lines, ["求职意向", "应聘岗位", "目标岗位", "期望职位"]),
        expected_salary=_find_labeled_value(lines, ["期望薪资", "薪资要求", "期望月薪"]),
        years_of_experience=_guess_experience(text),
        education=_guess_education(lines),
        work_experience=_guess_work_experience(lines),
        projects=_guess_projects(lines),
    )


def _find_first(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else None


def _find_labeled_value(lines: list[str], labels: list[str]) -> str | None:
    for line in lines:
        for label in labels:
            if label.lower() in line.lower():
                value = re.sub(rf"^{re.escape(label)}\s*[:：]?\s*", "", line, flags=re.IGNORECASE)
                return value.strip() or line
    return None


def _guess_name(lines: list[str]) -> str | None:
    skip_words = ("简历", "resume", "电话", "邮箱", "@", "求职", "地址")
    for line in lines[:8]:
        if any(word.lower() in line.lower() for word in skip_words):
            continue
        if 2 <= len(line) <= 12 and not re.search(r"\d", line):
            return line
    return None


def _guess_experience(text: str) -> str | None:
    return _find_first(r"\d+\s*年(?:以上)?(?:工作)?经验", text)


def _guess_education(lines: list[str]) -> list[dict[str, str | None]]:
    keywords = ("大学", "学院", "本科", "硕士", "博士", "专科", "Bachelor", "Master", "PhD")
    items = []
    for line in lines:
        if any(keyword.lower() in line.lower() for keyword in keywords):
            items.append({"school": line, "degree": None, "major": None, "period": None})
        if len(items) >= 3:
            break
    return items


def _guess_work_experience(lines: list[str]) -> list[dict[str, Any]]:
    section_keywords = ("工作经历", "工作经验", "实习经历", "任职经历", "Work Experience", "Experience")
    company_keywords = ("有限公司", "集团", "科技", "公司", "Co.", "Ltd", "Inc", "LLC")
    items = []

    for index, line in enumerate(lines):
        if any(keyword.lower() in line.lower() for keyword in section_keywords + company_keywords):
            context = lines[index : index + 5]
            description = " ".join(context)
            items.append(
                {
                    "company": _guess_company_from_line(line),
                    "position": _guess_position(context),
                    "period": _find_first(
                        r"(?:20\d{2}|19\d{2})[./年-]?\d{0,2}\s*(?:-|至|到|~)\s*(?:20\d{2}|19\d{2}|至今|现在|Present)",
                        description,
                    ),
                    "description": description[:300],
                    "highlights": _guess_highlights(context),
                    "technologies": [],
                }
            )
        if len(items) >= 3:
            break

    return items


def _guess_company_from_line(line: str) -> str | None:
    if any(keyword in line for keyword in ("有限公司", "集团", "科技", "公司")):
        return line[:80]
    if any(keyword.lower() in line.lower() for keyword in ("Co.", "Ltd", "Inc", "LLC")):
        return line[:80]
    return None


def _guess_position(lines: list[str]) -> str | None:
    position_keywords = ("工程师", "开发", "后端", "前端", "产品", "运营", "经理", "实习", "Engineer", "Developer")
    for line in lines:
        if any(keyword.lower() in line.lower() for keyword in position_keywords):
            return line[:80]
    return None


def _guess_highlights(lines: list[str]) -> list[str]:
    highlights = []
    for line in lines[1:]:
        if len(line) >= 8:
            highlights.append(line[:180])
        if len(highlights) >= 3:
            break
    return highlights


def _guess_projects(lines: list[str]) -> list[dict[str, Any]]:
    projects = []
    for index, line in enumerate(lines):
        if "项目" in line or "Project" in line:
            description = " ".join(lines[index : index + 3])
            projects.append(
                {
                    "name": line[:80],
                    "role": None,
                    "description": description[:300],
                    "highlights": [],
                    "technologies": [],
                }
            )
        if len(projects) >= 3:
            break
    return projects
