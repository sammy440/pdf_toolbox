"""
Read basic PDF metadata.
"""

from pathlib import Path
from typing import Dict, Union

from PyPDF2 import PdfReader

PathLike = Union[str, Path]


def read_metadata(input_path: PathLike) -> Dict[str, str]:
    """
    Return a simple dict of PDF metadata fields as strings.
    """
    reader = PdfReader(str(input_path))
    info = reader.metadata or {}
    result: Dict[str, str] = {}
    for key, value in info.items():
        # keys from PyPDF2 are like '/Title', '/Author', etc.
        clean_key = str(key).lstrip("/")
        result[clean_key] = "" if value is None else str(value)
    return result


