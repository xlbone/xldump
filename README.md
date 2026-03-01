# xldump

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/xlbone/xldump/graph/badge.svg)](https://codecov.io/gh/xlbone/xldump)

[English](./README.md) | [日本語](./README.ja.md) | [中文](./README.zh-CN.md)

A Python library and CLI tool that dumps the physical structure of Excel (.xlsx) files to JSON.

The core value is a wrapper that converts openpyxl Cell objects into structured dict/JSON.

## Features

- **Deterministic & Reproducible**: Extracts only physical structure without using LLM
- **openpyxl Compatible**: Field names aligned with openpyxl attribute names
- **Flexible Output Options**: Individual control for styles, values, merges, borders, validations, and images
- **NDA-Safe Mode**: Use `--no-values` to exclude cell values and safely extract only style structure

## Installation

```bash
pip install xldump
```

Or using uv:

```bash
uv add xldump
```

## CLI Usage

```bash
# List sheets
xldump scan design_doc.xlsx

# Dump all sheets
xldump dump design_doc.xlsx

# Specific sheets only
xldump dump design_doc.xlsx -s "Sheet1" "Sheet2"

# Style-only mode (no values = NDA-safe)
xldump dump design_doc.xlsx --no-values

# Output to file
xldump dump design_doc.xlsx -o output.json

# Compact output
xldump dump design_doc.xlsx --compact
```

## Library Usage

```python
import xldump

# Get sheet list (lightweight & fast)
sheets = xldump.scan("design_doc.xlsx")
for sheet in sheets:
    print(f"{sheet.name}: {sheet.max_row} rows x {sheet.max_column} cols")

# Dump entire workbook
workbook = xldump.dump("design_doc.xlsx")
print(workbook.to_dict())

# Dump single sheet
sheet = xldump.dump_sheet("design_doc.xlsx", "Sheet1")
print(sheet.to_dict())

# With options
workbook = xldump.dump(
    "design_doc.xlsx",
    sheets=["Sheet1", "Sheet2"],  # Target sheets
    include_styles=True,          # Style information
    include_values=True,          # Cell values
    include_merges=True,          # Merged cell information
    include_borders=True,         # Border information
    include_validations=True,     # Data validations
    include_images=True,          # Image position information
    data_only=False,              # Get calculated results instead of formulas
)
```

## Output Examples

### scan output

```json
{
  "file": "design_doc.xlsx",
  "sheet_count": 3,
  "sheets": [
    {
      "name": "Design",
      "index": 0,
      "dimensions": "A1:F30",
      "max_row": 30,
      "max_column": 6,
      "merged_cell_count": 12,
      "has_images": true,
      "has_data_validations": true
    }
  ]
}
```

### dump output

```json
{
  "file": "design_doc.xlsx",
  "sheets": [
    {
      "name": "Design",
      "index": 0,
      "dimensions": "A1:F30",
      "merged_cells": [
        {
          "range": "A1:D1",
          "min_row": 1, "max_row": 1,
          "min_col": 1, "max_col": 4
        }
      ],
      "rows": {
        "1": {
          "A": {
            "coordinate": "A1",
            "value": "1. System Overview",
            "data_type": "s",
            "style": {
              "font": {
                "name": "Arial",
                "size": 14.0,
                "bold": true
              },
              "fill": {
                "type": "solid",
                "fg_color": "FF4472C4"
              }
            }
          }
        }
      }
    }
  ]
}
```

## Development

```bash
# Clone repository
git clone https://github.com/xlbone/xldump.git
cd xldump

# Install dependencies
uv sync --all-groups

# Run tests
poe test

# Run all checks
poe check
```

## Notes

- Only `.xlsx` format is supported (legacy `.xls` format is not supported)
- `data_only=True` returns cached values from when the file was last opened in Excel. Returns `None` if not calculated

## License

MIT License
