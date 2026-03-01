"""Merged cell extraction utilities.

This module provides functions to extract merged cell information from
openpyxl worksheets.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from xldump.models import MergedCellInfo

if TYPE_CHECKING:
    from openpyxl.worksheet.worksheet import Worksheet


def extract_merged_cells(ws: Worksheet) -> list[MergedCellInfo]:
    """Extract all merged cell ranges from a worksheet.

    Args:
        ws: The openpyxl Worksheet to extract from.

    Returns:
        A list of MergedCellInfo objects representing each merged range.

    """
    merged_cells: list[MergedCellInfo] = []

    for merged_range in ws.merged_cells.ranges:
        merged_cells.append(
            MergedCellInfo(
                range=str(merged_range),
                min_row=merged_range.min_row,
                max_row=merged_range.max_row,
                min_col=merged_range.min_col,
                max_col=merged_range.max_col,
            )
        )

    return merged_cells
