"""Generate downloadable PDF analysis reports."""

import logging
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

logger = logging.getLogger(__name__)


def generate_report_pdf(
    output_path: Path,
    user_name: str,
    job_title: str,
    resume_filename: str,
    ats_score: float,
    semantic_similarity: float,
    keyword_match_rate: float,
    matched_skills: list[str],
    missing_skills: list[str],
    feedback: dict,
    suggestions: list[str],
    keyword_suggestions: list[str],
) -> Path:
    """Build a professional PDF report and return the file path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=22,
        textColor=colors.HexColor("#1e40af"),
        spaceAfter=12,
    )
    heading = styles["Heading2"]
    body = styles["BodyText"]

    story = [
        Paragraph("AI Resume Analyzer — Analysis Report", title_style),
        Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", body),
        Spacer(1, 0.2 * inch),
        Paragraph(f"<b>Candidate:</b> {user_name}", body),
        Paragraph(f"<b>Resume:</b> {resume_filename}", body),
        Paragraph(f"<b>Target Role:</b> {job_title or 'Not specified'}", body),
        Spacer(1, 0.3 * inch),
        Paragraph("ATS Compatibility Scores", heading),
    ]

    score_data = [
        ["Metric", "Score"],
        ["Overall ATS Score", f"{ats_score}%"],
        ["Semantic Similarity (BERT)", f"{semantic_similarity}%"],
        ["Keyword / Skill Match", f"{keyword_match_rate}%"],
    ]
    score_table = Table(score_data, colWidths=[3.5 * inch, 2 * inch])
    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
            ]
        )
    )
    story.append(score_table)
    story.append(Spacer(1, 0.25 * inch))

    story.append(Paragraph("Matched Skills", heading))
    story.append(Paragraph(", ".join(matched_skills) or "None detected", body))
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("Missing Skills", heading))
    story.append(Paragraph(", ".join(missing_skills) or "None — great match!", body))
    story.append(Spacer(1, 0.25 * inch))

    if feedback.get("summary"):
        story.append(Paragraph("AI Feedback Summary", heading))
        story.append(Paragraph(feedback["summary"], body))
        story.append(Spacer(1, 0.15 * inch))

    for section_key, title in [
        ("strengths", "Strengths"),
        ("weaknesses", "Areas to Improve"),
        ("ats_tips", "ATS Optimization Tips"),
    ]:
        items = feedback.get(section_key, [])
        if items:
            story.append(Paragraph(title, heading))
            for item in items:
                story.append(Paragraph(f"• {item}", body))
            story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("Improvement Suggestions", heading))
    for s in suggestions:
        story.append(Paragraph(f"• {s}", body))
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("Recommended Keywords", heading))
    story.append(Paragraph(", ".join(keyword_suggestions), body))

    doc.build(story)
    logger.info("PDF report saved: %s", output_path)
    return output_path
