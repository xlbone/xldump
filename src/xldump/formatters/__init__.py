"""Output formatters for xldump.

This module provides formatters to convert WorkbookDump data to various
output formats. Currently only JSON is supported.
"""

from xldump.formatters.base import OutputFormatter
from xldump.formatters.json import JsonFormatter

__all__ = [
    "OutputFormatter",
    "JsonFormatter",
]
