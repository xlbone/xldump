"""Base output formatter interface.

This module defines the abstract base class for output formatters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xldump.models import ScanResult, WorkbookDump


class OutputFormatter(ABC):
    """Abstract base class for output formatters.

    Output formatters convert WorkbookDump data to various string formats.
    Subclasses must implement the format() and format_to_file() methods.
    """

    @abstractmethod
    def format(
        self, data: WorkbookDump | ScanResult, *, include_values: bool = True
    ) -> str:
        """Convert data to a formatted string.

        Args:
            data: The WorkbookDump or ScanResult to format.
            include_values: If False, exclude cell values (style-only mode).

        Returns:
            The formatted string representation.

        """
        ...

    @abstractmethod
    def format_to_file(
        self,
        data: WorkbookDump | ScanResult,
        filepath: str | Path,
        *,
        include_values: bool = True,
    ) -> None:
        """Write formatted data to a file.

        Args:
            data: The WorkbookDump or ScanResult to format.
            filepath: The path to write to.
            include_values: If False, exclude cell values (style-only mode).

        """
        ...
