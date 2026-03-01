# 输出格式

[English](./output-format.md) | [日本語](./output-format.ja.md) | [中文](./output-format.zh-CN.md)

本文档介绍 xldump 的 JSON 输出格式。

## 概述

xldump 以 JSON 格式输出 Excel 文件结构。有两个主要命令，具有不同的输出结构：

- `scan`: 关于工作表的轻量级元数据
- `dump`: 包含单元格、样式等的完整结构导出

## scan 输出

`scan` 命令返回工作簿和工作表的元数据。

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

### 字段

| 字段 | 类型 | 描述 |
|------|------|------|
| `file` | string | 输入文件名 |
| `sheet_count` | integer | 工作簿中的工作表数量 |
| `sheets` | array | 工作表元数据对象数组 |

### 工作表元数据字段

| 字段 | 类型 | 描述 |
|------|------|------|
| `name` | string | 工作表名称 |
| `index` | integer | 从零开始的工作表索引 |
| `dimensions` | string | 使用范围（例如 "A1:F30"） |
| `max_row` | integer | 有数据的最大行号 |
| `max_column` | integer | 有数据的最大列号 |
| `merged_cell_count` | integer | 合并单元格范围数量 |
| `has_images` | boolean | 工作表是否包含图片 |
| `has_data_validations` | boolean | 工作表是否有数据验证规则 |

## dump 输出

`dump` 命令返回工作簿的完整结构。

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

### 工作表对象字段

| 字段 | 类型 | 描述 |
|------|------|------|
| `name` | string | 工作表名称 |
| `index` | integer | 从零开始的工作表索引 |
| `dimensions` | string | 使用范围 |
| `merged_cells` | array | 合并单元格范围（当 `include_merges=true` 时） |
| `data_validations` | array | 数据验证规则（当 `include_validations=true` 时） |
| `images` | array | 图片信息（当 `include_images=true` 时） |
| `rows` | object | 以行号为键的行数据 |

### 合并单元格

```json
{
  "range": "A1:D1",
  "min_row": 1,
  "max_row": 1,
  "min_col": 1,
  "max_col": 4
}
```

### 单元格对象

单元格嵌套在 `rows` → 行号 → 列字母 下：

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

### 单元格字段

| 字段 | 类型 | 描述 |
|------|------|------|
| `coordinate` | string | 单元格地址（例如 "A1"） |
| `value` | any | 单元格值（字符串、数字、布尔值、null） |
| `data_type` | string | openpyxl 数据类型代码 |
| `style` | object | 样式信息（当 `include_styles=true` 时） |

### 数据类型

| 代码 | 类型 |
|------|------|
| `s` | 字符串 |
| `n` | 数字 |
| `d` | 日期 |
| `b` | 布尔值 |
| `f` | 公式 |
| `e` | 错误 |

### 样式对象

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

### 边框样式

| 样式 | 描述 |
|------|------|
| `thin` | 细线 |
| `medium` | 中线 |
| `thick` | 粗线 |
| `dashed` | 虚线 |
| `dotted` | 点线 |
| `double` | 双线 |

## 颜色格式

颜色以 ARGB 十六进制字符串表示：

- `FF000000` = 黑色（完全不透明）
- `FFFFFFFF` = 白色（完全不透明）
- `FF4472C4` = 蓝色（主题颜色）

格式: `AARRGGBB`
- `AA`: Alpha（透明度）
- `RR`: 红色
- `GG`: 绿色
- `BB`: 蓝色
