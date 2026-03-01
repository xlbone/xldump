# xldump

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](./README.md) | [日本語](./README.ja.md) | [中文](./README.zh-CN.md)

Excel (.xlsx) ファイルの物理構造を JSON にダンプする Python ライブラリ＋CLI ツール。

openpyxl が提供する Cell オブジェクトを構造化 dict/JSON に変換するラッパーが中核価値です。

## 特徴

- **決定論的・再現可能**: LLM を一切使わず、物理構造のみを抽出
- **openpyxl 準拠**: フィールド名は openpyxl の属性名に合わせた設計
- **柔軟な出力オプション**: スタイル、値、結合、罫線、入力規則、画像の個別制御
- **NDA 対応モード**: `--no-values` でセル値を除外し、スタイル構造のみを安全に抽出

## インストール

```bash
pip install xldump
```

または uv を使用:

```bash
uv add xldump
```

## CLI 使用例

```bash
# シート一覧の確認
xldump scan design_doc.xlsx

# 全シートをダンプ
xldump dump design_doc.xlsx

# 特定シートのみ
xldump dump design_doc.xlsx -s "基本設計" "画面一覧"

# スタイルのみモード（値を含めない = NDA対応）
xldump dump design_doc.xlsx --no-values

# ファイル出力
xldump dump design_doc.xlsx -o output.json

# コンパクト出力
xldump dump design_doc.xlsx --compact
```

## ライブラリとして使用

```python
import xldump

# シート一覧を取得（軽量・高速）
sheets = xldump.scan("design_doc.xlsx")
for sheet in sheets:
    print(f"{sheet.name}: {sheet.max_row} rows x {sheet.max_column} cols")

# ワークブック全体をダンプ
workbook = xldump.dump("design_doc.xlsx")
print(workbook.to_dict())

# 単一シートをダンプ
sheet = xldump.dump_sheet("design_doc.xlsx", "基本設計")
print(sheet.to_dict())

# オプション指定
workbook = xldump.dump(
    "design_doc.xlsx",
    sheets=["Sheet1", "Sheet2"],  # 対象シート
    include_styles=True,          # スタイル情報
    include_values=True,          # セル値
    include_merges=True,          # セル結合情報
    include_borders=True,         # 罫線情報
    include_validations=True,     # 入力規則
    include_images=True,          # 画像位置情報
    data_only=False,              # 数式の代わりに計算結果を取得
)
```

## 出力例

### scan 出力

```json
{
  "file": "design_doc.xlsx",
  "sheet_count": 3,
  "sheets": [
    {
      "name": "基本設計",
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

### dump 出力

```json
{
  "file": "design_doc.xlsx",
  "sheets": [
    {
      "name": "基本設計",
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
            "value": "1. システム概要",
            "data_type": "s",
            "style": {
              "font": {
                "name": "メイリオ",
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

## 開発

```bash
# リポジトリをクローン
git clone https://github.com/xlbone/xldump.git
cd xldump

# 依存関係をインストール
uv sync --all-groups

# テスト実行
poe test

# 全チェック実行
poe check
```

## 注意事項

- `.xlsx` 形式のみ対応（`.xls` 旧形式は非対応）
- `data_only=True` は最後に Excel で開いた時点のキャッシュ値を返します。未計算の場合は `None` になります

## ライセンス

MIT License
