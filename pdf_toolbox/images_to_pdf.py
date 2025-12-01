"""
Convert images to a single PDF.
"""

from pathlib import Path
from typing import Iterable, List, Union

from PIL import Image

PathLike = Union[str, Path]


def images_to_pdf(image_paths: Iterable[PathLike], output_path: PathLike) -> Path:
    """
    Convert one or more image files into a single PDF.
    """
    paths: List[Path] = [Path(p) for p in image_paths]
    if not paths:
        raise ValueError("No image paths provided")

    # Open all images and convert to RGB
    images = [Image.open(p).convert("RGB") for p in paths]
    first, *rest = images

    out = Path(output_path)
    if out.suffix.lower() != ".pdf":
        out = out.with_suffix(".pdf")

    first.save(out, save_all=True, append_images=rest)
    return out


