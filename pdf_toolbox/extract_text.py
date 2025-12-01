"""
Extract text from PDF files.
"""

from pathlib import Path
from typing import Optional, Union

from PyPDF2 import PdfReader

PathLike = Union[str, Path]


def extract_text(
    input_path: PathLike, start_page: Optional[int] = None, end_page: Optional[int] = None
) -> str:
    """
    Extract text from a PDF.

    Pages are 1-based. If start_page/end_page are None, the full document is used.
    """
    reader = PdfReader(str(input_path))
    total_pages = len(reader.pages)

    if start_page is None:
        start_page = 1
    if end_page is None:
        end_page = total_pages

    start_i = max(start_page - 1, 0)
    end_i = min(end_page - 1, total_pages - 1)

    chunks = []
    for page_num in range(start_i, end_i + 1):
        page = reader.pages[page_num]
        chunks.append(page.extract_text() or "")
    return "\n".join(chunks)


