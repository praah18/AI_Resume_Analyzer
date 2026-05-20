"""Extract and match skills from resume and job description text."""

import re

from app.services.skills_taxonomy import ALL_SKILLS, SKILL_LOOKUP


def _normalize_text(text: str) -> str:
    return text.lower().replace("\n", " ")


def extract_skills_from_text(text: str) -> list[str]:
    """Find known skills mentioned in text using word-boundary matching."""
    normalized = _normalize_text(text)
    found: set[str] = set()

    for skill in ALL_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, normalized):
            found.add(SKILL_LOOKUP[skill.lower()])

    # Multi-word aliases
    aliases = {
        "node": "node.js",
        "react.js": "react",
        "vue.js": "vue",
        "amazon web services": "aws",
        "google cloud platform": "gcp",
        "ml": "machine learning",
        "ai": "generative ai",
    }
    for alias, canonical in aliases.items():
        if re.search(r"\b" + re.escape(alias) + r"\b", normalized):
            if canonical.lower() in SKILL_LOOKUP:
                found.add(SKILL_LOOKUP[canonical.lower()])

    return sorted(found)


def compare_skills(resume_skills: list[str], job_skills: list[str]) -> tuple[list[str], list[str]]:
    """Return matched and missing skills (job requirements not in resume)."""
    resume_set = {s.lower() for s in resume_skills}
    matched = [s for s in job_skills if s.lower() in resume_set]
    missing = [s for s in job_skills if s.lower() not in resume_set]
    return matched, missing


def keyword_match_rate(resume_text: str, job_text: str) -> float:
    """Ratio of job-description keywords found in resume (0-100)."""
    job_skills = extract_skills_from_text(job_text)
    if not job_skills:
        return 0.0
    resume_skills = extract_skills_from_text(resume_text)
    matched, _ = compare_skills(resume_skills, job_skills)
    return round((len(matched) / len(job_skills)) * 100, 2)
