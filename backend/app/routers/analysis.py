"""Resume analysis and history routes."""

import json
import logging
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.analysis import Analysis
from app.models.user import User
from app.schemas.analysis import AnalysisResponse, AnalysisSummary
from app.services.analysis_pipeline import run_analysis
from app.services.pdf_extractor import extract_text_from_pdf
from app.services.pdf_report import generate_report_pdf

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analysis", tags=["Resume Analysis"])

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(..., description="Resume PDF file"),
    job_description: str = Form(..., min_length=50),
    job_title: str = Form(""),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if resume.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await resume.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 10MB limit")
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    result = run_analysis(resume_text, job_description)

    settings = get_settings()
    report_dir = Path(settings.reports_dir)
    report_filename = f"report_{current_user.id}_{uuid4().hex[:8]}.pdf"
    report_path = report_dir / report_filename

    generate_report_pdf(
        output_path=report_path,
        user_name=current_user.full_name,
        job_title=job_title,
        resume_filename=resume.filename or "resume.pdf",
        ats_score=result.ats_score,
        semantic_similarity=result.semantic_similarity,
        keyword_match_rate=result.keyword_match_rate,
        matched_skills=result.matched_skills,
        missing_skills=result.missing_skills,
        feedback=result.feedback,
        suggestions=result.suggestions,
        keyword_suggestions=result.keyword_suggestions,
    )

    record = Analysis(
        user_id=current_user.id,
        resume_filename=resume.filename or "resume.pdf",
        job_title=job_title,
        ats_score=result.ats_score,
        semantic_similarity=result.semantic_similarity,
        keyword_match_rate=result.keyword_match_rate,
        matched_skills_json=json.dumps(result.matched_skills),
        missing_skills_json=json.dumps(result.missing_skills),
        feedback_json=json.dumps(result.feedback),
        suggestions_json=json.dumps(result.suggestions),
        keyword_suggestions_json=json.dumps(result.keyword_suggestions),
        report_path=str(report_path),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return _to_response(record, result.semantic_similarity, result.keyword_match_rate)


@router.get("/history", response_model=list[AnalysisSummary])
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Analysis)
        .filter(Analysis.user_id == current_user.id)
        .order_by(Analysis.created_at.desc())
        .limit(50)
        .all()
    )
    return rows


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return _to_response(record, record.semantic_similarity, record.keyword_match_rate)


@router.get("/{analysis_id}/report")
def download_report(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id)
        .first()
    )
    if not record or not record.report_path:
        raise HTTPException(status_code=404, detail="Report not found")

    path = Path(record.report_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report file missing on server")

    return FileResponse(
        path,
        media_type="application/pdf",
        filename=f"resume_analysis_{analysis_id}.pdf",
    )


def _to_response(record: Analysis, semantic: float, keyword: float) -> AnalysisResponse:
    report_url = f"/api/analysis/{record.id}/report" if record.report_path else None
    return AnalysisResponse(
        id=record.id,
        resume_filename=record.resume_filename,
        job_title=record.job_title,
        ats_score=record.ats_score,
        matched_skills=record.matched_skills,
        missing_skills=record.missing_skills,
        feedback=record.feedback,
        suggestions=record.suggestions,
        keyword_suggestions=record.keyword_suggestions,
        semantic_similarity=semantic,
        keyword_match_rate=keyword,
        created_at=record.created_at,
        report_url=report_url,
    )
