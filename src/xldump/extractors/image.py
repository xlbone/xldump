"""Image extraction utilities.

This module provides functions to extract image position information from
openpyxl worksheets.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from openpyxl.utils import get_column_letter

from xldump.models import ImageInfo

if TYPE_CHECKING:
    from openpyxl.worksheet.worksheet import Worksheet


def extract_images(ws: Worksheet) -> list[ImageInfo]:
    """Extract all image position information from a worksheet.

    Args:
        ws: The openpyxl Worksheet to extract from.

    Returns:
        A list of ImageInfo objects representing all images in the worksheet.

    """
    images: list[ImageInfo] = []

    # Access images through the _images attribute
    for img in ws._images:
        anchor_str = _get_anchor_string(img.anchor)
        image_info = ImageInfo(
            anchor=anchor_str,
            width=img.width if img.width else None,
            height=img.height if img.height else None,
            description="",  # openpyxl doesn't provide easy access to alt text
        )
        images.append(image_info)

    return images


def _get_anchor_string(anchor: Any) -> str:
    """Convert an image anchor to a cell coordinate string.

    Args:
        anchor: The anchor object (string, OneCellAnchor, or TwoCellAnchor).

    Returns:
        A cell coordinate string (e.g., "B2").

    """
    # If anchor is already a string (e.g., "B2"), return it directly
    if isinstance(anchor, str):
        return anchor

    # Handle OneCellAnchor or TwoCellAnchor with _from attribute
    if hasattr(anchor, "_from"):
        from_marker = anchor._from
        # Column and row are 0-based in the anchor
        col = get_column_letter(from_marker.col + 1)
        row = from_marker.row + 1
        return f"{col}{row}"

    # Fallback
    return "A1"


def has_images(ws: Worksheet) -> bool:
    """Check if a worksheet has any images.

    Args:
        ws: The openpyxl Worksheet to check.

    Returns:
        True if the worksheet has images, False otherwise.

    """
    return len(ws._images) > 0
