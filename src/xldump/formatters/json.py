"""JSON output formatter.

This module provides the JSON formatter for xldump output.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from xldump.formatters.base import OutputFormatter
from xldump.models import ScanResult, WorkbookDump


class JsonFormatter(OutputFormatter):
    """JSON output formatter.

    Formats WorkbookDump or ScanResult data as JSON strings.
    """

    def __init__(self, *, indent: int | None = 2, ensure_ascii: bool = False) -> None:
        """Initialize the JSON formatter.

        Args:
            indent: Number of spaces for indentation. None for compact output.
            ensure_ascii: If True, escape non-ASCII characters.

        """
        self.indent = indent
        self.ensure_ascii = ensure_ascii

    def format(
        self, data: WorkbookDump | ScanResult, *, include_values: bool = True
    ) -> str:
        """Convert data to a JSON string.

        Args:
            data: The WorkbookDump or ScanResult to format.
            include_values: If False, exclude cell values (style-only mode).

        Returns:
            The JSON string representation.

        """
        # Use different to_dict methods based on data type
        if isinstance(data, WorkbookDump):
            dict_data = data.to_dict(include_values=include_values)
        else:
            # ScanResult doesn't have include_values option
            dict_data = data.to_dict()

        return json.dumps(
            dict_data,
            indent=self.indent,
            ensure_ascii=self.ensure_ascii,
            default=self._json_serializer,
        )

    def format_to_file(
        self,
        data: WorkbookDump | ScanResult,
        filepath: str | Path,
        *,
        include_values: bool = True,
    ) -> None:
        """Write formatted data to a JSON file.

        Args:
            data: The WorkbookDump or ScanResult to format.
            filepath: The path to write to.
            include_values: If False, exclude cell values (style-only mode).

        """
        content = self.format(data, include_values=include_values)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def _json_serializer(self, obj: Any) -> Any:
        """Serialize objects not serializable by default JSON encoder.

        Args:
            obj: The object to serialize.

        Returns:
            A JSON-serializable representation of the object.

        """
        # Handle datetime objects
        if hasattr(obj, "isoformat"):
            return obj.isoformat()

        # Handle bytes
        if isinstance(obj, bytes):
            return obj.decode("utf-8", errors="replace")

        # Default: convert to string
        return str(obj)
