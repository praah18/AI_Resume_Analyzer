"""Sentence-transformer embeddings and cosine similarity for ATS scoring."""

import logging
from functools import lru_cache

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.config import get_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_model():
    """Load embedding model once (cached)."""
    from sentence_transformers import SentenceTransformer

    settings = get_settings()
    logger.info("Loading embedding model: %s", settings.embedding_model)
    return SentenceTransformer(settings.embedding_model)


def get_embeddings(texts: list[str]) -> np.ndarray:
    model = _get_model()
    return model.encode(texts, convert_to_numpy=True, show_progress_bar=False)


def semantic_similarity_score(resume_text: str, job_text: str) -> float:
    """
    Cosine similarity between resume and job description embeddings.
    Returns percentage 0-100.
    """
    embeddings = get_embeddings([resume_text[:8000], job_text[:8000]])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(float(similarity) * 100, 2)


def compute_ats_score(semantic_score: float, keyword_rate: float) -> float:
    """
    Combined ATS score: 70% semantic similarity + 30% keyword/skill match.
    """
    combined = (semantic_score * 0.7) + (keyword_rate * 0.3)
    return round(min(max(combined, 0), 100), 2)
