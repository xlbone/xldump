"""Data models for xldump.

This module defines dataclasses that represent Excel workbook structures.
Field names follow openpyxl conventions for familiarity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class FontInfo:
    """Font style information."""

    name: str | None = None
    size: float | None = None
    bold: bool = False
    italic: bool = False
    color: str | None = None  # ARGB hex

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values."""
        return {
            k: v for k, v in asdict(self).items() if v is not None and v is not False
        }


@dataclass
class FillInfo:
    """Cell fill (background) information."""

    type: str | None = None  # "solid", "pattern", etc.
    fg_color: str | None = None  # ARGB hex

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class AlignmentInfo:
    """Cell alignment information."""

    horizontal: str | None = None
    vertical: str | None = None
    wrap_text: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values and False."""
        return {
            k: v for k, v in asdict(self).items() if v is not None and v is not False
        }


@dataclass
class BorderSideInfo:
    """Single border side information."""

    style: str | None = None  # "thin", "medium", "thick", etc.
    color: str | None = None  # ARGB hex

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class BorderInfo:
    """Cell border information (all four sides)."""

    top: BorderSideInfo | None = None
    bottom: BorderSideInfo | None = None
    left: BorderSideInfo | None = None
    right: BorderSideInfo | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values."""
        result: dict[str, Any] = {}
        if self.top:
            top_dict = self.top.to_dict()
            if top_dict:
                result["top"] = top_dict
        if self.bottom:
            bottom_dict = self.bottom.to_dict()
            if bottom_dict:
                result["bottom"] = bottom_dict
        if self.left:
            left_dict = self.left.to_dict()
            if left_dict:
                result["left"] = left_dict
        if self.right:
            right_dict = self.right.to_dict()
            if right_dict:
                result["right"] = right_dict
        return result


@dataclass
class ProtectionInfo:
    """Cell protection information."""

    locked: bool = True
    hidden: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict."""
        return asdict(self)


@dataclass
class CellStyle:
    """Complete cell style information."""

    font: FontInfo | None = None
    fill: FillInfo | None = None
    alignment: AlignmentInfo | None = None
    border: BorderInfo | None = None
    number_format: str = "General"
    protection: ProtectionInfo | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values and empty dicts."""
        result: dict[str, Any] = {}
        if self.font:
            font_dict = self.font.to_dict()
            if font_dict:
                result["font"] = font_dict
        if self.fill:
            fill_dict = self.fill.to_dict()
            if fill_dict:
                result["fill"] = fill_dict
        if self.alignment:
            alignment_dict = self.alignment.to_dict()
            if alignment_dict:
                result["alignment"] = alignment_dict
        if self.border:
            border_dict = self.border.to_dict()
            if border_dict:
                result["border"] = border_dict
        if self.number_format and self.number_format != "General":
            result["number_format"] = self.number_format
        if self.protection:
            result["protection"] = self.protection.to_dict()
        return result


@dataclass
class CellDump:
    """Dumped cell information including value and style."""

    coordinate: str
    value: Any = None
    data_type: str = "n"
    style: CellStyle | None = None

    def to_dict(self, *, include_values: bool = True) -> dict[str, Any]:
        """Convert to dict, excluding None values.

        Args:
            include_values: If False, exclude the value field (style-only mode).

        """
        result: dict[str, Any] = {"coordinate": self.coordinate}
        if include_values:
            result["value"] = self.value
        result["data_type"] = self.data_type
        if self.style:
            style_dict = self.style.to_dict()
            if style_dict:
                result["style"] = style_dict
        return result


@dataclass
class MergedCellInfo:
    """Merged cell range information."""

    range: str
    min_row: int
    max_row: int
    min_col: int
    max_col: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict."""
        return asdict(self)


@dataclass
class DataValidationInfo:
    """Data validation rule information."""

    range: str
    type: str | None = None
    formula1: str | None = None
    formula2: str | None = None
    allow_blank: bool = True
    prompt: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values."""
        result: dict[str, Any] = {"range": self.range}
        if self.type:
            result["type"] = self.type
        if self.formula1:
            result["formula1"] = self.formula1
        if self.formula2:
            result["formula2"] = self.formula2
        result["allow_blank"] = self.allow_blank
        if self.prompt:
            result["prompt"] = self.prompt
        if self.error:
            result["error"] = self.error
        return result


@dataclass
class ImageInfo:
    """Image position information."""

    anchor: str
    width: int | None = None
    height: int | None = None
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values."""
        result: dict[str, Any] = {"anchor": self.anchor}
        if self.width is not None:
            result["width"] = self.width
        if self.height is not None:
            result["height"] = self.height
        if self.description:
            result["description"] = self.description
        return result


@dataclass
class SheetInfo:
    """Lightweight sheet information for scan operation."""

    name: str
    index: int
    dimensions: str | None = None
    max_row: int = 0
    max_column: int = 0
    merged_cell_count: int = 0
    has_images: bool = False
    has_data_validations: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict."""
        return {
            "name": self.name,
            "index": self.index,
            "dimensions": self.dimensions,
            "max_row": self.max_row,
            "max_column": self.max_column,
            "merged_cell_count": self.merged_cell_count,
            "has_images": self.has_images,
            "has_data_validations": self.has_data_validations,
        }


@dataclass
class SheetDump:
    """Complete sheet information for dump operation."""

    name: str
    index: int
    dimensions: str | None = None
    max_row: int = 0
    max_column: int = 0
    merged_cells: list[MergedCellInfo] = field(default_factory=list)
    data_validations: list[DataValidationInfo] = field(default_factory=list)
    images: list[ImageInfo] = field(default_factory=list)
    rows: dict[str, dict[str, CellDump | None]] = field(default_factory=dict)

    def to_dict(self, *, include_values: bool = True) -> dict[str, Any]:
        """Convert to dict.

        Args:
            include_values: If False, exclude cell values (style-only mode).

        """
        result: dict[str, Any] = {
            "name": self.name,
            "index": self.index,
            "dimensions": self.dimensions,
            "max_row": self.max_row,
            "max_column": self.max_column,
        }
        if self.merged_cells:
            result["merged_cells"] = [mc.to_dict() for mc in self.merged_cells]
        if self.data_validations:
            result["data_validations"] = [dv.to_dict() for dv in self.data_validations]
        if self.images:
            result["images"] = [img.to_dict() for img in self.images]
        if self.rows:
            rows_dict: dict[str, dict[str, Any]] = {}
            for row_num, cols in self.rows.items():
                cols_dict: dict[str, Any] = {}
                for col_letter, cell in cols.items():
                    if cell is None:
                        cols_dict[col_letter] = None
                    else:
                        cols_dict[col_letter] = cell.to_dict(
                            include_values=include_values
                        )
                rows_dict[row_num] = cols_dict
            result["rows"] = rows_dict
        return result


@dataclass
class WorkbookDump:
    """Complete workbook dump information."""

    file: str
    sheets: list[SheetDump] = field(default_factory=list)
    sheet_count: int = 0

    def to_dict(self, *, include_values: bool = True) -> dict[str, Any]:
        """Convert to dict.

        Args:
            include_values: If False, exclude cell values (style-only mode).

        """
        return {
            "file": self.file,
            "sheet_count": self.sheet_count,
            "sheets": [s.to_dict(include_values=include_values) for s in self.sheets],
        }


@dataclass
class ScanResult:
    """Result of scan operation."""

    file: str
    sheet_count: int
    sheets: list[SheetInfo] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict."""
        return {
            "file": self.file,
            "sheet_count": self.sheet_count,
            "sheets": [s.to_dict() for s in self.sheets],
        }
