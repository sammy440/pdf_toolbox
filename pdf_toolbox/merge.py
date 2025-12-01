"""
Merge PDF operation.
"""

from pathlib import Path
from typing import Iterable, Union

from .utils import merge_pdfs

PathLike = Union[str, Path]


def merge_files(input_paths: Iterable[PathLike], output_path: PathLike) -> Path:
    """
    Merge multiple PDF files into a single output PDF.

    This is a thin wrapper around `utils.merge_pdfs` so the GUI
    can call one simple function.
    """

    return merge_pdfs(input_paths, output_path)


