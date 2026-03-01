"""Tests for xldump.formatters module."""

from __future__ import annotations

import json
from pathlib import Path

from xldump import dump, scan
from xldump.formatters import JsonFormatter


class TestJsonFormatter:
    """Tests for JsonFormatter class."""

    def test_format_scan_result(self, simple_table_path: Path) -> None:
        """Test formatting ScanResult as JSON."""
        result = scan(simple_table_path)
        formatter = JsonFormatter()

        output = formatter.format(result)

        # Verify it's valid JSON
        parsed = json.loads(output)
        assert "file" in parsed
        assert "sheet_count" in parsed
        assert "sheets" in parsed

    def test_format_workbook_dump(self, simple_table_path: Path) -> None:
        """Test formatting WorkbookDump as JSON."""
        result = dump(simple_table_path)
        formatter = JsonFormatter()

        output = formatter.format(result)

        # Verify it's valid JSON
        parsed = json.loads(output)
        assert "file" in parsed
        assert "sheets" in parsed
        assert len(parsed["sheets"]) > 0

    def test_format_with_indent(self, simple_table_path: Path) -> None:
        """Test formatting with custom indent."""
        result = scan(simple_table_path)
        formatter = JsonFormatter(indent=4)

        output = formatter.format(result)

        # With indent, output should have multiple lines
        assert output.count("\n") > 1

    def test_format_compact(self, simple_table_path: Path) -> None:
        """Test formatting with no indent (compact)."""
        result = scan(simple_table_path)
        formatter = JsonFormatter(indent=None)

        output = formatter.format(result)

        # Compact output should be single line (or minimal lines)
        # Note: JSON may still have a trailing newline
        assert output.count("\n") <= 1

    def test_format_ensure_ascii(self, simple_table_path: Path) -> None:
        """Test formatting with ensure_ascii option."""
        result = scan(simple_table_path)

        # Test with ensure_ascii=False (default)
        formatter = JsonFormatter(ensure_ascii=False)
        output = formatter.format(result)
        assert isinstance(output, str)

        # Test with ensure_ascii=True
        formatter = JsonFormatter(ensure_ascii=True)
        output = formatter.format(result)
        assert isinstance(output, str)

    def test_format_to_file(self, simple_table_path: Path, tmp_path: Path) -> None:
        """Test writing formatted output to file."""
        result = dump(simple_table_path)
        formatter = JsonFormatter()

        output_file = tmp_path / "output.json"
        formatter.format_to_file(result, output_file)

        # Verify file exists and contains valid JSON
        assert output_file.exists()
        content = json.loads(output_file.read_text())
        assert "file" in content
        assert "sheets" in content

    def test_format_no_values(self, simple_table_path: Path) -> None:
        """Test formatting with include_values=False."""
        result = dump(simple_table_path)
        formatter = JsonFormatter()

        output = formatter.format(result, include_values=False)
        parsed = json.loads(output)

        # Verify cells don't have value field
        sheets = parsed.get("sheets", [])
        if sheets:
            rows = sheets[0].get("rows", {})
            for row in rows.values():
                for cell in row.values():
                    if cell is not None:
                        assert "value" not in cell


class TestJsonFormatterCustomTypes:
    """Tests for JsonFormatter handling of custom types."""

    def test_datetime_serialization(self) -> None:
        """Test that datetime objects are serialized correctly."""
        from datetime import datetime

        from xldump.models import CellDump, SheetDump, WorkbookDump

        cell = CellDump(
            coordinate="A1",
            value=datetime(2024, 1, 15, 10, 30, 0),
            data_type="d",
        )
        sheet = SheetDump(
            name="Sheet1",
            index=0,
            rows={"1": {"A": cell}},
        )
        workbook = WorkbookDump(
            file="test.xlsx",
            sheets=[sheet],
            sheet_count=1,
        )

        formatter = JsonFormatter()
        output = formatter.format(workbook)

        # Should not raise and produce valid JSON
        parsed = json.loads(output)
        assert parsed is not None
