"""Tests for xldump.cli module."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


class TestCLIScan:
    """Tests for the scan CLI command."""

    def test_scan_command(self, simple_table_path: Path) -> None:
        """Test basic scan command output."""
        result = subprocess.run(
            [sys.executable, "-m", "xldump.cli", "scan", str(simple_table_path)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        # Parse output as JSON
        output = json.loads(result.stdout)
        assert "file" in output
        assert "sheet_count" in output
        assert "sheets" in output

    def test_scan_compact_output(self, simple_table_path: Path) -> None:
        """Test scan with compact JSON output."""
        result = subprocess.run(
            [sys.executable, "-m", "xldump.cli", "scan", str(simple_table_path), "--compact"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        # Compact output should not have newlines (except trailing)
        assert result.stdout.count("\n") <= 1

    def test_scan_nonexistent_file(self, fixtures_dir: Path) -> None:
        """Test scan with nonexistent file."""
        result = subprocess.run(
            [sys.executable, "-m", "xldump.cli", "scan", str(fixtures_dir / "nonexistent.xlsx")],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert "Error" in result.stderr


class TestCLIDump:
    """Tests for the dump CLI command."""

    def test_dump_command(self, simple_table_path: Path) -> None:
        """Test basic dump command output."""
        result = subprocess.run(
            [sys.executable, "-m", "xldump.cli", "dump", str(simple_table_path)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        # Parse output as JSON
        output = json.loads(result.stdout)
        assert "file" in output
        assert "sheets" in output
        assert len(output["sheets"]) > 0

    def test_dump_specific_sheets(self, multi_sheet_path: Path) -> None:
        """Test dump with specific sheet filter."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "xldump.cli",
                "dump",
                str(multi_sheet_path),
                "-s",
                "Summary",
                "Data",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        output = json.loads(result.stdout)
        sheet_names = [s["name"] for s in output["sheets"]]
        assert "Summary" in sheet_names
        assert "Data" in sheet_names
        assert "Notes" not in sheet_names

    def test_dump_no_styles(self, styled_cells_path: Path) -> None:
        """Test dump without styles."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "xldump.cli",
                "dump",
                str(styled_cells_path),
                "--no-styles",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        output = json.loads(result.stdout)
        # Check that cells don't have style info
        sheet = output["sheets"][0]
        if sheet.get("rows"):
            for row in sheet["rows"].values():
                for cell in row.values():
                    if cell is not None:
                        assert "style" not in cell

    def test_dump_no_values(self, simple_table_path: Path) -> None:
        """Test dump without cell values."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "xldump.cli",
                "dump",
                str(simple_table_path),
                "--no-values",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        output = json.loads(result.stdout)
        # Check that cells don't have values
        sheet = output["sheets"][0]
        if sheet.get("rows"):
            for row in sheet["rows"].values():
                for cell in row.values():
                    if cell is not None:
                        assert "value" not in cell

    def test_dump_compact_output(self, simple_table_path: Path) -> None:
        """Test dump with compact JSON output."""
        result = subprocess.run(
            [sys.executable, "-m", "xldump.cli", "dump", str(simple_table_path), "--compact"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        # Compact output should be a single line
        assert result.stdout.count("\n") <= 1

    def test_dump_to_file(self, simple_table_path: Path, tmp_path: Path) -> None:
        """Test dump output to file."""
        output_file = tmp_path / "output.json"

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "xldump.cli",
                "dump",
                str(simple_table_path),
                "-o",
                str(output_file),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert output_file.exists()

        # Verify file content is valid JSON
        content = json.loads(output_file.read_text())
        assert "file" in content
        assert "sheets" in content


class TestCLIHelp:
    """Tests for CLI help messages."""

    def test_help(self) -> None:
        """Test --help flag."""
        result = subprocess.run(
            [sys.executable, "-m", "xldump.cli", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "xldump" in result.stdout.lower()
        assert "scan" in result.stdout
        assert "dump" in result.stdout

    def test_scan_help(self) -> None:
        """Test scan --help."""
        result = subprocess.run(
            [sys.executable, "-m", "xldump.cli", "scan", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "scan" in result.stdout.lower()

    def test_dump_help(self) -> None:
        """Test dump --help."""
        result = subprocess.run(
            [sys.executable, "-m", "xldump.cli", "dump", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "dump" in result.stdout.lower()
        assert "--sheets" in result.stdout or "-s" in result.stdout
