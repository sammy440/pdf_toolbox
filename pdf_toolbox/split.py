"""
Split PDF operation.
"""

from pathlib import Path
from typing import Iterable, List, Tuple, Union

from PyPDF2 import PdfReader, PdfWriter

PathLike = Union[str, Path]


def split_by_ranges(
    input_path: PathLike, ranges: Iterable[Tuple[int, int]], output_dir: PathLike
) -> List[Path]:
    """
    Split a PDF into multiple PDFs by 1-based inclusive page ranges.

    Example ranges: [(1, 3), (4, 4), (5, 10)]
    """
    src = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(src))
    results: List[Path] = []

    for idx, (start, end) in enumerate(ranges, start=1):
        writer = PdfWriter()
        # Clamp to valid page indices
        start_i = max(start - 1, 0)
        end_i = min(end - 1, len(reader.pages) - 1)
        for page_num in range(start_i, end_i + 1):
            writer.add_page(reader.pages[page_num])

        out_path = output_dir / f"{src.stem}_part{idx}.pdf"
        with out_path.open("wb") as f:
            writer.write(f)
        results.append(out_path)

    return results


