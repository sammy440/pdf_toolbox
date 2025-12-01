"""
Shared utilities for PDF operations.
"""

from pathlib import Path
from typing import Iterable, Union

from PyPDF2 import PdfReader, PdfWriter


PathLike = Union[str, Path]


def ensure_pdf_suffix(path: PathLike) -> Path:
    """Return a Path with `.pdf` extension ensured."""
    p = Path(path)
    if p.suffix.lower() != ".pdf":
        p = p.with_suffix(".pdf")
    return p


def merge_pdfs(input_paths: Iterable[PathLike], output_path: PathLike) -> Path:
    """Simple merge utility used by GUI and tests."""
    writer = PdfWriter()
    for p in input_paths:
        reader = PdfReader(str(p))
        for page in reader.pages:
            writer.add_page(page)
    out = ensure_pdf_suffix(output_path)
    with out.open("wb") as f:
        writer.write(f)
    return out


