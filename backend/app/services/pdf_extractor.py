"""Extract plain text from uploaded PDF resumes."""

import logging
from io import BytesIO

from pypdf import PdfReader

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Read PDF bytes and return concatenated page text."""
    try:
        reader = PdfReader(BytesIO(file_bytes))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        content = "\n".join(pages).strip()
        if not content:
            raise ValueError("No text could be extracted from the PDF. It may be scanned/image-only.")
        return content
    except Exception as exc:
        logger.exception("PDF extraction failed")
        raise ValueError(f"Failed to read PDF: {exc}") from exc
