"""Pydantic schemas for resume analysis endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field


class AnalysisCreate(BaseModel):
    job_description: str = Field(min_length=50)
    job_title: str = Field(default="", max_length=255)


class AnalysisResponse(BaseModel):
    id: int
    resume_filename: str
    job_title: str
    ats_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    feedback: dict
    suggestions: list[str]
    keyword_suggestions: list[str]
    semantic_similarity: float
    keyword_match_rate: float
    created_at: datetime
    report_url: str | None = None

    model_config = {"from_attributes": True}


class AnalysisSummary(BaseModel):
    id: int
    resume_filename: str
    job_title: str
    ats_score: float
    created_at: datetime

    model_config = {"from_attributes": True}
