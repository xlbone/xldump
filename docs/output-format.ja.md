# 出力フォーマット

[English](./output-format.md) | [日本語](./output-format.ja.md) | [中文](./output-format.zh-CN.md)

このドキュメントでは、xldump の JSON 出力フォーマットについて説明します。

## 概要

xldump は Excel ファイルの構造を JSON 形式で出力します。2つのメインコマンドがあり、それぞれ異なる出力構造を持ちます：

- `scan`: シートに関する軽量なメタデータ
- `dump`: セル、スタイルなどを含む完全な構造ダンプ

## scan 出力

`scan` コマンドはワークブックとシートのメタデータを返します。

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

### フィールド

| フィールド | 型 | 説明 |
|------------|------|-------------|
| `file` | string | 入力ファイル名 |
| `sheet_count` | integer | ワークブック内のシート数 |
| `sheets` | array | シートメタデータオブジェクトの配列 |

### シートメタデータフィールド

| フィールド | 型 | 説明 |
|------------|------|-------------|
| `name` | string | シート名 |
| `index` | integer | 0始まりのシートインデックス |
| `dimensions` | string | 使用範囲（例: "A1:F30"） |
| `max_row` | integer | データがある最大行番号 |
| `max_column` | integer | データがある最大列番号 |
| `merged_cell_count` | integer | 結合セル範囲の数 |
| `has_images` | boolean | シートに画像が含まれているか |
| `has_data_validations` | boolean | シートに入力規則があるか |

## dump 出力

`dump` コマンドはワークブックの完全な構造を返します。

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

### シートオブジェクトフィールド

| フィールド | 型 | 説明 |
|------------|------|-------------|
| `name` | string | シート名 |
| `index` | integer | 0始まりのシートインデックス |
| `dimensions` | string | 使用範囲 |
| `merged_cells` | array | 結合セル範囲（`include_merges=true` の場合） |
| `data_validations` | array | 入力規則（`include_validations=true` の場合） |
| `images` | array | 画像情報（`include_images=true` の場合） |
| `rows` | object | 行番号をキーとした行データ |

### 結合セル

```json
{
  "range": "A1:D1",
  "min_row": 1,
  "max_row": 1,
  "min_col": 1,
  "max_col": 4
}
```

### セルオブジェクト

セルは `rows` → 行番号 → 列文字 の下にネストされます：

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

### セルフィールド

| フィールド | 型 | 説明 |
|------------|------|-------------|
| `coordinate` | string | セルアドレス（例: "A1"） |
| `value` | any | セル値（文字列、数値、真偽値、null） |
| `data_type` | string | openpyxl のデータ型コード |
| `style` | object | スタイル情報（`include_styles=true` の場合） |

### データ型

| コード | 型 |
|--------|------|
| `s` | 文字列 |
| `n` | 数値 |
| `d` | 日付 |
| `b` | 真偽値 |
| `f` | 数式 |
| `e` | エラー |

### スタイルオブジェクト

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

### 罫線スタイル

| スタイル | 説明 |
|----------|-------------|
| `thin` | 細線 |
| `medium` | 中線 |
| `thick` | 太線 |
| `dashed` | 破線 |
| `dotted` | 点線 |
| `double` | 二重線 |

## 色フォーマット

色は ARGB 16進数文字列で表されます：

- `FF000000` = 黒（完全不透明）
- `FFFFFFFF` = 白（完全不透明）
- `FF4472C4` = 青（テーマカラー）

フォーマット: `AARRGGBB`
- `AA`: アルファ（透明度）
- `RR`: 赤
- `GG`: 緑
- `BB`: 青
