"""Resume analysis history ORM model."""

import json
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    resume_filename: Mapped[str] = mapped_column(String(512), nullable=False)
    job_title: Mapped[str] = mapped_column(String(255), default="")
    ats_score: Mapped[float] = mapped_column(nullable=False)
    semantic_similarity: Mapped[float] = mapped_column(default=0.0)
    keyword_match_rate: Mapped[float] = mapped_column(default=0.0)
    matched_skills_json: Mapped[str] = mapped_column(Text, default="[]")
    missing_skills_json: Mapped[str] = mapped_column(Text, default="[]")
    feedback_json: Mapped[str] = mapped_column(Text, default="{}")
    suggestions_json: Mapped[str] = mapped_column(Text, default="[]")
    keyword_suggestions_json: Mapped[str] = mapped_column(Text, default="[]")
    report_path: Mapped[str] = mapped_column(String(1024), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="analyses")

    @property
    def matched_skills(self) -> list:
        return json.loads(self.matched_skills_json or "[]")

    @property
    def missing_skills(self) -> list:
        return json.loads(self.missing_skills_json or "[]")

    @property
    def feedback(self) -> dict:
        return json.loads(self.feedback_json or "{}")

    @property
    def suggestions(self) -> list:
        return json.loads(self.suggestions_json or "[]")

    @property
    def keyword_suggestions(self) -> list:
        return json.loads(self.keyword_suggestions_json or "[]")
