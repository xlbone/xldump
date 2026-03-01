# xldump

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/xlbone/xldump/graph/badge.svg)](https://codecov.io/gh/xlbone/xldump)

[English](./README.md) | [日本語](./README.ja.md) | [中文](./README.zh-CN.md)

将 Excel (.xlsx) 文件的物理结构导出为 JSON 的 Python 库和 CLI 工具。

核心价值是将 openpyxl 的 Cell 对象转换为结构化 dict/JSON 的封装器。

## 特性

- **确定性和可重现性**: 不使用 LLM，仅提取物理结构
- **兼容 openpyxl**: 字段名与 openpyxl 属性名保持一致
- **灵活的输出选项**: 可单独控制样式、值、合并单元格、边框、数据验证和图片
- **NDA 安全模式**: 使用 `--no-values` 排除单元格值，安全地仅提取样式结构

## 安装

```bash
pip install xldump
```

或使用 uv：

```bash
uv add xldump
```

## CLI 使用示例

```bash
# 查看工作表列表
xldump scan design_doc.xlsx

# 导出所有工作表
xldump dump design_doc.xlsx

# 仅导出指定工作表
xldump dump design_doc.xlsx -s "Sheet1" "Sheet2"

# 仅样式模式（不含值 = NDA 安全）
xldump dump design_doc.xlsx --no-values

# 输出到文件
xldump dump design_doc.xlsx -o output.json

# 紧凑输出
xldump dump design_doc.xlsx --compact
```

## 作为库使用

```python
import xldump

# 获取工作表列表（轻量且快速）
sheets = xldump.scan("design_doc.xlsx")
for sheet in sheets:
    print(f"{sheet.name}: {sheet.max_row} 行 x {sheet.max_column} 列")

# 导出整个工作簿
workbook = xldump.dump("design_doc.xlsx")
print(workbook.to_dict())

# 导出单个工作表
sheet = xldump.dump_sheet("design_doc.xlsx", "Sheet1")
print(sheet.to_dict())

# 使用选项
workbook = xldump.dump(
    "design_doc.xlsx",
    sheets=["Sheet1", "Sheet2"],  # 目标工作表
    include_styles=True,          # 样式信息
    include_values=True,          # 单元格值
    include_merges=True,          # 合并单元格信息
    include_borders=True,         # 边框信息
    include_validations=True,     # 数据验证
    include_images=True,          # 图片位置信息
    data_only=False,              # 获取计算结果而非公式
)
```

## 输出示例

### scan 输出

```json
{
  "file": "design_doc.xlsx",
  "sheet_count": 3,
  "sheets": [
    {
      "name": "设计",
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

### dump 输出

```json
{
  "file": "design_doc.xlsx",
  "sheets": [
    {
      "name": "设计",
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
            "value": "1. 系统概述",
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

## 开发

```bash
# 克隆仓库
git clone https://github.com/xlbone/xldump.git
cd xldump

# 安装依赖
uv sync --all-groups

# 运行测试
poe test

# 运行所有检查
poe check
```

## 注意事项

- 仅支持 `.xlsx` 格式（不支持旧版 `.xls` 格式）
- `data_only=True` 返回文件最后在 Excel 中打开时的缓存值。如果未计算则返回 `None`

## 许可证

MIT License
