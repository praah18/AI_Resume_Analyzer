"""Orchestrates the full resume analysis pipeline."""

import json
import logging
from dataclasses import dataclass

from app.services.embedding_service import compute_ats_score, semantic_similarity_score
from app.services.gemini_service import generate_ai_feedback, generate_suggestions
from app.services.skill_extractor import (
    compare_skills,
    extract_skills_from_text,
    keyword_match_rate,
)

logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    ats_score: float
    semantic_similarity: float
    keyword_match_rate: float
    matched_skills: list[str]
    missing_skills: list[str]
    feedback: dict
    suggestions: list[str]
    keyword_suggestions: list[str]


def run_analysis(resume_text: str, job_description: str) -> AnalysisResult:
    """Execute embedding, skill, and AI analysis on resume vs job description."""
    logger.info("Starting resume analysis pipeline")

    resume_skills = extract_skills_from_text(resume_text)
    job_skills = extract_skills_from_text(job_description)
    matched, missing = compare_skills(resume_skills, job_skills)

    semantic = semantic_similarity_score(resume_text, job_description)
    keyword_rate = keyword_match_rate(resume_text, job_description)
    ats_score = compute_ats_score(semantic, keyword_rate)

    feedback = generate_ai_feedback(
        resume_text, job_description, matched, missing, ats_score
    )
    suggestions, keyword_suggestions = generate_suggestions(
        resume_text, job_description, missing
    )

    logger.info("Analysis complete — ATS score: %.2f", ats_score)

    return AnalysisResult(
        ats_score=ats_score,
        semantic_similarity=semantic,
        keyword_match_rate=keyword_rate,
        matched_skills=matched,
        missing_skills=missing,
        feedback=feedback,
        suggestions=suggestions,
        keyword_suggestions=keyword_suggestions,
    )


def result_to_storage_dict(result: AnalysisResult) -> dict:
    """Serialize analysis result for database persistence."""
    return {
        "ats_score": result.ats_score,
        "matched_skills_json": json.dumps(result.matched_skills),
        "missing_skills_json": json.dumps(result.missing_skills),
        "feedback_json": json.dumps(result.feedback),
        "suggestions_json": json.dumps(result.suggestions),
        "keyword_suggestions_json": json.dumps(result.keyword_suggestions),
    }
