"""Tests for xldump.core module."""

from __future__ import annotations

from pathlib import Path

import pytest

from xldump import dump, dump_sheet, scan
from xldump.core import FileNotFoundError, InvalidFileError


class TestScan:
    """Tests for the scan() function."""

    def test_scan_simple_table(self, simple_table_path: Path) -> None:
        """Test scanning a simple table workbook."""
        result = scan(simple_table_path)

        assert result.file == "simple_table.xlsx"
        assert result.sheet_count == 1
        assert len(result.sheets) == 1

        sheet = result.sheets[0]
        assert sheet.name == "Sheet1"
        assert sheet.index == 0
        assert sheet.max_row >= 4
        assert sheet.max_column >= 3

    def test_scan_multi_sheet(self, multi_sheet_path: Path) -> None:
        """Test scanning a workbook with multiple sheets."""
        result = scan(multi_sheet_path)

        assert result.sheet_count == 3
        assert len(result.sheets) == 3

        sheet_names = [s.name for s in result.sheets]
        assert "Summary" in sheet_names
        assert "Data" in sheet_names
        assert "Notes" in sheet_names

    def test_scan_merged_cells(self, merged_cells_path: Path) -> None:
        """Test scanning a workbook with merged cells."""
        result = scan(merged_cells_path)

        sheet = result.sheets[0]
        assert sheet.merged_cell_count > 0

    def test_scan_nonexistent_file(self, fixtures_dir: Path) -> None:
        """Test scanning a nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            scan(fixtures_dir / "nonexistent.xlsx")

    def test_scan_invalid_extension(self, fixtures_dir: Path) -> None:
        """Test scanning a file with invalid extension raises error."""
        # Create a temporary text file
        invalid_file = fixtures_dir / "invalid.txt"
        invalid_file.write_text("not an excel file")
        try:
            with pytest.raises(InvalidFileError):
                scan(invalid_file)
        finally:
            invalid_file.unlink()


class TestDump:
    """Tests for the dump() function."""

    def test_dump_simple_table(self, simple_table_path: Path) -> None:
        """Test dumping a simple table workbook."""
        result = dump(simple_table_path)

        assert result.file == "simple_table.xlsx"
        assert result.sheet_count == 1
        assert len(result.sheets) == 1

        sheet = result.sheets[0]
        assert sheet.name == "Sheet1"

        # Check that rows were extracted
        assert len(sheet.rows) > 0

        # Check first row has header data
        if "1" in sheet.rows:
            row1 = sheet.rows["1"]
            assert "A" in row1
            cell = row1["A"]
            assert cell is not None
            assert cell.value == "ID"

    def test_dump_with_sheet_filter(self, multi_sheet_path: Path) -> None:
        """Test dumping specific sheets only."""
        result = dump(multi_sheet_path, sheets=["Summary", "Data"])

        assert result.sheet_count == 2
        sheet_names = [s.name for s in result.sheets]
        assert "Summary" in sheet_names
        assert "Data" in sheet_names
        assert "Notes" not in sheet_names

    def test_dump_merged_cells(self, merged_cells_path: Path) -> None:
        """Test dumping workbook with merged cells."""
        result = dump(merged_cells_path)

        sheet = result.sheets[0]
        assert len(sheet.merged_cells) > 0

        # Check that merged cell range is captured
        ranges = [mc.range for mc in sheet.merged_cells]
        assert any("A1" in r for r in ranges)

    def test_dump_styled_cells(self, styled_cells_path: Path) -> None:
        """Test dumping workbook with styled cells."""
        result = dump(styled_cells_path)

        sheet = result.sheets[0]

        # Check that cell A1 has bold font
        if "1" in sheet.rows and "A" in sheet.rows["1"]:
            cell = sheet.rows["1"]["A"]
            assert cell is not None
            assert cell.style is not None
            assert cell.style.font is not None
            assert cell.style.font.bold is True

    def test_dump_no_styles(self, styled_cells_path: Path) -> None:
        """Test dumping without styles."""
        result = dump(styled_cells_path, include_styles=False)

        sheet = result.sheets[0]
        if "1" in sheet.rows and "A" in sheet.rows["1"]:
            cell = sheet.rows["1"]["A"]
            assert cell is not None
            assert cell.style is None

    def test_dump_no_values(self, simple_table_path: Path) -> None:
        """Test dumping without values (style-only mode)."""
        result = dump(simple_table_path, include_values=False)

        sheet = result.sheets[0]
        if "1" in sheet.rows and "A" in sheet.rows["1"]:
            cell = sheet.rows["1"]["A"]
            assert cell is not None
            assert cell.value is None

    def test_dump_no_merges(self, merged_cells_path: Path) -> None:
        """Test dumping without merge information."""
        result = dump(merged_cells_path, include_merges=False)

        sheet = result.sheets[0]
        assert len(sheet.merged_cells) == 0


class TestDumpSheet:
    """Tests for the dump_sheet() function."""

    def test_dump_single_sheet(self, multi_sheet_path: Path) -> None:
        """Test dumping a single sheet."""
        sheet = dump_sheet(multi_sheet_path, "Data")

        assert sheet.name == "Data"
        assert len(sheet.rows) > 0

    def test_dump_nonexistent_sheet(self, simple_table_path: Path) -> None:
        """Test dumping a nonexistent sheet raises error."""
        with pytest.raises(ValueError, match="not found"):
            dump_sheet(simple_table_path, "NonexistentSheet")


class TestToDict:
    """Tests for to_dict() methods."""

    def test_scan_result_to_dict(self, simple_table_path: Path) -> None:
        """Test ScanResult.to_dict() produces valid dict."""
        result = scan(simple_table_path)
        d = result.to_dict()

        assert isinstance(d, dict)
        assert "file" in d
        assert "sheet_count" in d
        assert "sheets" in d
        assert isinstance(d["sheets"], list)

    def test_workbook_dump_to_dict(self, simple_table_path: Path) -> None:
        """Test WorkbookDump.to_dict() produces valid dict."""
        result = dump(simple_table_path)
        d = result.to_dict()

        assert isinstance(d, dict)
        assert "file" in d
        assert "sheet_count" in d
        assert "sheets" in d
        assert isinstance(d["sheets"], list)

        if d["sheets"]:
            sheet = d["sheets"][0]
            assert "name" in sheet
            assert "rows" in sheet

    def test_workbook_dump_to_dict_no_values(self, simple_table_path: Path) -> None:
        """Test WorkbookDump.to_dict() with include_values=False."""
        result = dump(simple_table_path)
        d = result.to_dict(include_values=False)

        # Check that cell values are excluded
        if d["sheets"]:
            sheet = d["sheets"][0]
            if sheet.get("rows"):
                for row in sheet["rows"].values():
                    for cell in row.values():
                        if cell is not None:
                            assert "value" not in cell
