"""Tests for xldump.extractors module."""

from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook

from xldump.extractors import extract_cells, extract_merged_cells, extract_sheet_info


class TestExtractCells:
    """Tests for extract_cells() function."""

    def test_extract_simple_cells(self, simple_table_path: Path) -> None:
        """Test extracting cells from simple table."""
        wb = load_workbook(simple_table_path)
        ws = wb.active
        assert ws is not None

        rows = extract_cells(ws)

        # Check that rows were extracted
        assert len(rows) > 0

        # Check header row
        assert "1" in rows
        row1 = rows["1"]
        assert "A" in row1
        assert row1["A"] is not None
        assert row1["A"].value == "ID"

        wb.close()

    def test_extract_cells_with_styles(self, styled_cells_path: Path) -> None:
        """Test extracting cells with style information."""
        wb = load_workbook(styled_cells_path)
        ws = wb.active
        assert ws is not None

        rows = extract_cells(ws, include_styles=True)

        # Check cell A1 has bold font
        assert "1" in rows
        assert "A" in rows["1"]
        cell = rows["1"]["A"]
        assert cell is not None
        assert cell.style is not None
        assert cell.style.font is not None
        assert cell.style.font.bold is True

        wb.close()

    def test_extract_cells_no_styles(self, styled_cells_path: Path) -> None:
        """Test extracting cells without style information."""
        wb = load_workbook(styled_cells_path)
        ws = wb.active
        assert ws is not None

        rows = extract_cells(ws, include_styles=False)

        # Check that style is None
        for row in rows.values():
            for cell in row.values():
                if cell is not None:
                    assert cell.style is None

        wb.close()

    def test_extract_cells_no_values(self, simple_table_path: Path) -> None:
        """Test extracting cells without values."""
        wb = load_workbook(simple_table_path)
        ws = wb.active
        assert ws is not None

        rows = extract_cells(ws, include_values=False)

        # Check that values are None
        for row in rows.values():
            for cell in row.values():
                if cell is not None:
                    assert cell.value is None

        wb.close()

    def test_extract_merged_cells_content(self, merged_cells_path: Path) -> None:
        """Test that merged cells have correct structure."""
        wb = load_workbook(merged_cells_path)
        ws = wb.active
        assert ws is not None

        rows = extract_cells(ws)

        # The merged range A1:D1 should have value in A1 only
        assert "1" in rows
        assert "A" in rows["1"]

        # A1 should have the value
        a1 = rows["1"]["A"]
        assert a1 is not None
        assert a1.value == "Section Title"

        # B1, C1, D1 should be None (part of merge, not top-left)
        if "B" in rows["1"]:
            assert rows["1"]["B"] is None
        if "C" in rows["1"]:
            assert rows["1"]["C"] is None
        if "D" in rows["1"]:
            assert rows["1"]["D"] is None

        wb.close()


class TestExtractMergedCells:
    """Tests for extract_merged_cells() function."""

    def test_extract_merged_cells(self, merged_cells_path: Path) -> None:
        """Test extracting merged cell ranges."""
        wb = load_workbook(merged_cells_path)
        ws = wb.active
        assert ws is not None

        merged = extract_merged_cells(ws)

        assert len(merged) > 0

        # Check that A1:D1 merge is captured
        ranges = [mc.range for mc in merged]
        assert any("A1" in r and "D1" in r for r in ranges)

        # Check merge info structure
        for mc in merged:
            assert mc.min_row > 0
            assert mc.max_row >= mc.min_row
            assert mc.min_col > 0
            assert mc.max_col >= mc.min_col

        wb.close()

    def test_no_merged_cells(self, simple_table_path: Path) -> None:
        """Test extracting from workbook without merged cells."""
        wb = load_workbook(simple_table_path)
        ws = wb.active
        assert ws is not None

        merged = extract_merged_cells(ws)

        assert len(merged) == 0

        wb.close()


class TestExtractSheetInfo:
    """Tests for extract_sheet_info() function."""

    def test_extract_sheet_info(self, simple_table_path: Path) -> None:
        """Test extracting sheet info."""
        wb = load_workbook(simple_table_path, read_only=False)
        ws = wb.active
        assert ws is not None

        info = extract_sheet_info(ws, 0)

        assert info.name == "Sheet1"
        assert info.index == 0
        assert info.max_row >= 4
        assert info.max_column >= 3

        wb.close()

    def test_extract_sheet_info_with_merges(self, merged_cells_path: Path) -> None:
        """Test sheet info includes merged cell count."""
        wb = load_workbook(merged_cells_path, read_only=False)
        ws = wb.active
        assert ws is not None

        info = extract_sheet_info(ws, 0)

        assert info.merged_cell_count > 0

        wb.close()
