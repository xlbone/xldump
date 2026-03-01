"""Data models for xldump.

This module defines Pydantic models that represent Excel workbook structures.
Field names follow openpyxl conventions for familiarity.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class FontInfo(BaseModel):
    """Font style information."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    size: float | None = None
    bold: bool = False
    italic: bool = False
    color: str | None = None  # ARGB hex

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values and False."""
        return {
            k: v
            for k, v in self.model_dump().items()
            if v is not None and v is not False
        }


class FillInfo(BaseModel):
    """Cell fill (background) information."""

    model_config = ConfigDict(extra="forbid")

    type: str | None = None  # "solid", "pattern", etc.
    fg_color: str | None = None  # ARGB hex

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values."""
        return self.model_dump(exclude_none=True)


class AlignmentInfo(BaseModel):
    """Cell alignment information."""

    model_config = ConfigDict(extra="forbid")

    horizontal: str | None = None
    vertical: str | None = None
    wrap_text: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values and False."""
        return {
            k: v
            for k, v in self.model_dump().items()
            if v is not None and v is not False
        }


class BorderSideInfo(BaseModel):
    """Single border side information."""

    model_config = ConfigDict(extra="forbid")

    style: str | None = None  # "thin", "medium", "thick", etc.
    color: str | None = None  # ARGB hex

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values."""
        return self.model_dump(exclude_none=True)


class BorderInfo(BaseModel):
    """Cell border information (all four sides)."""

    model_config = ConfigDict(extra="forbid")

    top: BorderSideInfo | None = None
    bottom: BorderSideInfo | None = None
    left: BorderSideInfo | None = None
    right: BorderSideInfo | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values and empty dicts."""
        result: dict[str, Any] = {}
        for side in ("top", "bottom", "left", "right"):
            side_info = getattr(self, side)
            if side_info:
                side_dict = side_info.to_dict()
                if side_dict:
                    result[side] = side_dict
        return result


class ProtectionInfo(BaseModel):
    """Cell protection information."""

    model_config = ConfigDict(extra="forbid")

    locked: bool = True
    hidden: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict."""
        return self.model_dump()


class CellStyle(BaseModel):
    """Complete cell style information."""

    model_config = ConfigDict(extra="forbid")

    font: FontInfo | None = None
    fill: FillInfo | None = None
    alignment: AlignmentInfo | None = None
    border: BorderInfo | None = None
    number_format: str = "General"
    protection: ProtectionInfo | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values and empty dicts."""
        result: dict[str, Any] = {}
        for field_name in ("font", "fill", "alignment", "border"):
            field_value = getattr(self, field_name)
            if field_value:
                field_dict = field_value.to_dict()
                if field_dict:
                    result[field_name] = field_dict
        if self.number_format and self.number_format != "General":
            result["number_format"] = self.number_format
        if self.protection:
            result["protection"] = self.protection.to_dict()
        return result


class CellDump(BaseModel):
    """Dumped cell information including value and style."""

    model_config = ConfigDict(extra="forbid")

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


class MergedCellInfo(BaseModel):
    """Merged cell range information."""

    model_config = ConfigDict(extra="forbid")

    range: str
    min_row: int
    max_row: int
    min_col: int
    max_col: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict."""
        return self.model_dump()


class DataValidationInfo(BaseModel):
    """Data validation rule information."""

    model_config = ConfigDict(extra="forbid")

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


class ImageInfo(BaseModel):
    """Image position information."""

    model_config = ConfigDict(extra="forbid")

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


class SheetInfo(BaseModel):
    """Lightweight sheet information for scan operation."""

    model_config = ConfigDict(extra="forbid")

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
        return self.model_dump()


class SheetDump(BaseModel):
    """Complete sheet information for dump operation."""

    model_config = ConfigDict(extra="forbid")

    name: str
    index: int
    dimensions: str | None = None
    max_row: int = 0
    max_column: int = 0
    merged_cells: list[MergedCellInfo] = []
    data_validations: list[DataValidationInfo] = []
    images: list[ImageInfo] = []
    rows: dict[str, dict[str, CellDump | None]] = {}

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


class WorkbookDump(BaseModel):
    """Complete workbook dump information."""

    model_config = ConfigDict(extra="forbid")

    file: str
    sheets: list[SheetDump] = []
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


class ScanResult(BaseModel):
    """Result of scan operation."""

    model_config = ConfigDict(extra="forbid")

    file: str
    sheet_count: int
    sheets: list[SheetInfo] = []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict."""
        return {
            "file": self.file,
            "sheet_count": self.sheet_count,
            "sheets": [s.to_dict() for s in self.sheets],
        }
