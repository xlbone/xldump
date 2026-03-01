# Output Format

[English](./output-format.md) | [日本語](./output-format.ja.md) | [中文](./output-format.zh-CN.md)

This document describes the JSON output format of xldump.

## Overview

xldump outputs Excel file structure in JSON format. There are two main commands with different output structures:

- `scan`: Lightweight metadata about sheets
- `dump`: Full structural dump including cells, styles, and more

## scan Output

The `scan` command returns metadata about the workbook and its sheets.

```json
{
  "file": "example.xlsx",
  "sheet_count": 3,
  "sheets": [
    {
      "name": "Sheet1",
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

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `file` | string | Input file name |
| `sheet_count` | integer | Number of sheets in workbook |
| `sheets` | array | Array of sheet metadata objects |

### Sheet Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Sheet name |
| `index` | integer | Zero-based sheet index |
| `dimensions` | string | Used range (e.g., "A1:F30") |
| `max_row` | integer | Maximum row number with data |
| `max_column` | integer | Maximum column number with data |
| `merged_cell_count` | integer | Number of merged cell ranges |
| `has_images` | boolean | Whether sheet contains images |
| `has_data_validations` | boolean | Whether sheet has data validation rules |

## dump Output

The `dump` command returns the full structure of the workbook.

```json
{
  "file": "example.xlsx",
  "sheets": [
    {
      "name": "Sheet1",
      "index": 0,
      "dimensions": "A1:F30",
      "merged_cells": [...],
      "data_validations": [...],
      "images": [...],
      "rows": {...}
    }
  ]
}
```

### Sheet Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Sheet name |
| `index` | integer | Zero-based sheet index |
| `dimensions` | string | Used range |
| `merged_cells` | array | Merged cell ranges (when `include_merges=true`) |
| `data_validations` | array | Data validation rules (when `include_validations=true`) |
| `images` | array | Image information (when `include_images=true`) |
| `rows` | object | Row data keyed by row number |

### Merged Cells

```json
{
  "range": "A1:D1",
  "min_row": 1,
  "max_row": 1,
  "min_col": 1,
  "max_col": 4
}
```

### Cell Object

Cells are nested under `rows` → row number → column letter:

```json
{
  "rows": {
    "1": {
      "A": {
        "coordinate": "A1",
        "value": "Hello",
        "data_type": "s",
        "style": {...}
      }
    }
  }
}
```

### Cell Fields

| Field | Type | Description |
|-------|------|-------------|
| `coordinate` | string | Cell address (e.g., "A1") |
| `value` | any | Cell value (string, number, boolean, null) |
| `data_type` | string | openpyxl data type code |
| `style` | object | Style information (when `include_styles=true`) |

### Data Types

| Code | Type |
|------|------|
| `s` | String |
| `n` | Number |
| `d` | Date |
| `b` | Boolean |
| `f` | Formula |
| `e` | Error |

### Style Object

```json
{
  "style": {
    "font": {
      "name": "Arial",
      "size": 11.0,
      "bold": false,
      "italic": false,
      "underline": "none",
      "color": "FF000000"
    },
    "fill": {
      "type": "solid",
      "fg_color": "FFFFFF00",
      "bg_color": "FF000000"
    },
    "alignment": {
      "horizontal": "left",
      "vertical": "center",
      "wrap_text": false
    },
    "border": {
      "left": {"style": "thin", "color": "FF000000"},
      "right": {"style": "thin", "color": "FF000000"},
      "top": {"style": "thin", "color": "FF000000"},
      "bottom": {"style": "thin", "color": "FF000000"}
    }
  }
}
```

### Border Styles

| Style | Description |
|-------|-------------|
| `thin` | Thin line |
| `medium` | Medium line |
| `thick` | Thick line |
| `dashed` | Dashed line |
| `dotted` | Dotted line |
| `double` | Double line |

## Color Format

Colors are represented as ARGB hex strings:

- `FF000000` = Black (fully opaque)
- `FFFFFFFF` = White (fully opaque)
- `FF4472C4` = Blue (theme color)

Format: `AARRGGBB`
- `AA`: Alpha (transparency)
- `RR`: Red
- `GG`: Green
- `BB`: Blue
