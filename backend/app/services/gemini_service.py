"""Google Gemini API integration for resume feedback and suggestions."""

import json
import logging
import re

from app.config import get_settings

logger = logging.getLogger(__name__)


def _get_client():
    import google.generativeai as genai

    settings = get_settings()
    if not settings.gemini_api_key:
        return None
    genai.configure(api_key=settings.gemini_api_key)
    return genai.GenerativeModel(settings.gemini_model)


def _parse_json_response(text: str) -> dict:
    """Extract JSON object from model response."""
    text = text.strip()
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Extract from markdown code block
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {}


def generate_ai_feedback(
    resume_text: str,
    job_text: str,
    matched_skills: list[str],
    missing_skills: list[str],
    ats_score: float,
) -> dict:
    """
    Call Gemini for structured feedback. Falls back to rule-based feedback
    when API key is missing or the request fails.
    """
    settings = get_settings()
    fallback = _fallback_feedback(matched_skills, missing_skills, ats_score)

    if not settings.gemini_api_key:
        logger.warning("GEMINI_API_KEY not set; using fallback feedback")
        return fallback

    model = _get_client()
    if model is None:
        return fallback

    prompt = f"""You are an expert ATS resume coach. Analyze this resume against the job description.

ATS Score: {ats_score}%
Matched Skills: {', '.join(matched_skills) or 'None'}
Missing Skills: {', '.join(missing_skills) or 'None'}

JOB DESCRIPTION (excerpt):
{job_text[:3000]}

RESUME (excerpt):
{resume_text[:3000]}

Respond ONLY with valid JSON (no markdown):
{{
  "summary": "2-3 sentence overall assessment",
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "ats_tips": ["tip 1", "tip 2", "tip 3"]
}}"""

    try:
        response = model.generate_content(prompt)
        parsed = _parse_json_response(response.text or "")
        if parsed.get("summary"):
            return parsed
        logger.warning("Gemini returned empty structure; using fallback")
        return fallback
    except Exception:
        logger.exception("Gemini API call failed")
        return fallback


def generate_suggestions(
    resume_text: str,
    job_text: str,
    missing_skills: list[str],
) -> tuple[list[str], list[str]]:
    """Return improvement suggestions and keyword optimization tips."""
    settings = get_settings()
    base_suggestions = _fallback_suggestions(missing_skills)
    base_keywords = _fallback_keywords(missing_skills, job_text)

    if not settings.gemini_api_key:
        return base_suggestions, base_keywords

    model = _get_client()
    if model is None:
        return base_suggestions, base_keywords

    prompt = f"""As a resume optimization expert, provide actionable improvements.

Missing skills: {', '.join(missing_skills) or 'none identified'}

JOB DESCRIPTION:
{job_text[:2500]}

RESUME:
{resume_text[:2500]}

Respond ONLY with valid JSON:
{{
  "suggestions": ["5 specific bullet-point improvements for the resume"],
  "keyword_suggestions": ["8 ATS keywords/phrases to add naturally"]
}}"""

    try:
        response = model.generate_content(prompt)
        parsed = _parse_json_response(response.text or "")
        suggestions = parsed.get("suggestions") or base_suggestions
        keywords = parsed.get("keyword_suggestions") or base_keywords
        return list(suggestions)[:8], list(keywords)[:12]
    except Exception:
        logger.exception("Gemini suggestions failed")
        return base_suggestions, base_keywords


def _fallback_feedback(matched: list[str], missing: list[str], score: float) -> dict:
    summary = (
        f"Your resume shows an ATS compatibility score of {score}%. "
        f"You match {len(matched)} required skills"
        + (f" but are missing {len(missing)} key skills." if missing else ".")
    )
    return {
        "summary": summary,
        "strengths": [
            f"Strong alignment on: {', '.join(matched[:5])}" if matched else "Clear professional structure",
            "Relevant experience sections detected",
            "Readable formatting for ATS parsers",
        ],
        "weaknesses": [
            f"Missing critical skills: {', '.join(missing[:5])}" if missing else "Consider adding more quantified achievements",
            "Ensure job-specific keywords appear in experience bullets",
            "Tailor summary/objective to the target role",
        ],
        "ats_tips": [
            "Use standard section headings (Experience, Education, Skills)",
            "Include exact skill names from the job posting",
            "Add measurable outcomes (%, $, time saved)",
            "Avoid tables, text boxes, and graphics that break ATS parsing",
        ],
    }


def _fallback_suggestions(missing: list[str]) -> list[str]:
    items = [
        "Rewrite your professional summary to mirror the job title and top 3 requirements.",
        "Add a dedicated Skills section with exact keywords from the job description.",
        "Quantify achievements with metrics (revenue, users, latency, team size).",
        "Place the most relevant experience and projects near the top of the resume.",
    ]
    if missing:
        items.insert(0, f"Incorporate these missing skills where truthful: {', '.join(missing[:6])}")
    return items[:6]


def _fallback_keywords(missing: list[str], job_text: str) -> list[str]:
    from app.services.skill_extractor import extract_skills_from_text

    job_skills = extract_skills_from_text(job_text)
    keywords = list(dict.fromkeys(missing + job_skills))[:12]
    return keywords or ["leadership", "cross-functional", "stakeholder management", "agile delivery"]
