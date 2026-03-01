"""xldump - Dump Excel (.xlsx) physical structure to JSON.

This library provides tools to extract the physical structure of Excel
workbooks, including cell values, styles, merged cells, and more.

Example usage:

    >>> import xldump
    >>> # Scan a workbook for sheet information
    >>> result = xldump.scan("example.xlsx")
    >>> print(result.sheet_count)
    3

    >>> # Dump full workbook structure
    >>> workbook = xldump.dump("example.xlsx")
    >>> print(workbook.sheets[0].name)
    "Sheet1"

    >>> # Dump a single sheet
    >>> sheet = xldump.dump_sheet("example.xlsx", "Sheet1")
    >>> print(sheet.max_row)
    100
"""

from xldump.core import dump, dump_sheet, scan
from xldump.formatters import JsonFormatter, OutputFormatter
from xldump.models import (
    CellDump,
    CellStyle,
    MergedCellInfo,
    ScanResult,
    SheetDump,
    SheetInfo,
    WorkbookDump,
)

__version__ = "0.1.0"
__all__ = [
    # Core functions
    "scan",
    "dump",
    "dump_sheet",
    # Data models
    "ScanResult",
    "WorkbookDump",
    "SheetDump",
    "SheetInfo",
    "CellDump",
    "CellStyle",
    "MergedCellInfo",
    # Formatters
    "JsonFormatter",
    "OutputFormatter",
]
