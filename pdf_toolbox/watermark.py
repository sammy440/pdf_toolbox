"""
Apply watermark to each page of a PDF.
"""

from pathlib import Path
from typing import Union

from PyPDF2 import PdfReader, PdfWriter

PathLike = Union[str, Path]


def apply_watermark(
    input_path: PathLike, watermark_path: PathLike, output_path: PathLike
) -> Path:
    """
    Overlay watermark PDF on each page of the input PDF.

    The watermark file's first page is used.
    """
    input_reader = PdfReader(str(input_path))
    watermark_reader = PdfReader(str(watermark_path))
    watermark_page = watermark_reader.pages[0]

    writer = PdfWriter()
    for page in input_reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    out = Path(output_path)
    if out.suffix.lower() != ".pdf":
        out = out.with_suffix(".pdf")
    with out.open("wb") as f:
        writer.write(f)
    return out


