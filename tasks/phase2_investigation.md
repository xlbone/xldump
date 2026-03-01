# Phase 2 調査結果

## 概要

Phase 2で実装する機能のopenpyxl API調査結果。

## 1. Data Validation (入力規則)

### アクセス方法

```python
# ワークシートの入力規則リストにアクセス
ws.data_validations.dataValidation  # List[DataValidation]
```

### DataValidation オブジェクト属性

| 属性 | 型 | 説明 |
|------|-----|------|
| `type` | str | 検証タイプ: list, whole, decimal, date, time, textLength, custom |
| `operator` | str | 演算子: between, notBetween, equal, notEqual, lessThan, lessThanOrEqual, greaterThan, greaterThanOrEqual |
| `formula1` | str | 検証式1（リストの場合は `"値1,値2,値3"` 形式） |
| `formula2` | str | 検証式2（between等で使用） |
| `allow_blank` | bool | 空白を許可するか |
| `showErrorMessage` | bool | エラーメッセージを表示するか |
| `error` | str | エラーメッセージ本文 |
| `errorTitle` | str | エラーメッセージタイトル |
| `showInputMessage` | bool | 入力メッセージを表示するか |
| `prompt` | str | 入力時のプロンプトメッセージ |
| `promptTitle` | str | プロンプトタイトル |
| `sqref` | MultiCellRange | 適用範囲（例: "A1:A10"） |

### 実装方針

```python
def extract_validations(ws: Worksheet) -> list[DataValidationInfo]:
    validations = []
    for dv in ws.data_validations.dataValidation:
        validations.append(DataValidationInfo(
            range=str(dv.sqref),
            type=dv.type,
            operator=dv.operator,
            formula1=dv.formula1,
            formula2=dv.formula2,
            allow_blank=dv.allow_blank,
            prompt=dv.prompt,
            error=dv.error,
        ))
    return validations
```

## 2. Images (画像)

### アクセス方法

```python
# ワークシートの画像リストにアクセス
ws._images  # List[Image]
```

### Image オブジェクト属性

| 属性 | 型 | 説明 |
|------|-----|------|
| `anchor` | str or OneCellAnchor or TwoCellAnchor | アンカー位置 |
| `width` | int | 幅（ピクセル） |
| `height` | int | 高さ（ピクセル） |
| `path` | str | 画像ファイルパス |

### アンカー詳細

ファイル読み込み後、anchorは `OneCellAnchor` または `TwoCellAnchor` オブジェクトになる。

```python
# OneCellAnchor の場合
anchor._from.col   # 列インデックス (0-based)
anchor._from.row   # 行インデックス (0-based)
anchor._from.colOff  # 列オフセット (EMU)
anchor._from.rowOff  # 行オフセット (EMU)
```

### EMU変換

- 1 inch = 914400 EMU
- 1 pixel (96 DPI) = 9525 EMU

### 実装方針

```python
def extract_images(ws: Worksheet) -> list[ImageInfo]:
    images = []
    for img in ws._images:
        anchor_str = _get_anchor_string(img.anchor)
        images.append(ImageInfo(
            anchor=anchor_str,
            width=img.width,
            height=img.height,
            description=""  # openpyxlでは直接取得できない
        ))
    return images

def _get_anchor_string(anchor) -> str:
    if isinstance(anchor, str):
        return anchor
    elif hasattr(anchor, '_from'):
        from openpyxl.utils import get_column_letter
        col = get_column_letter(anchor._from.col + 1)
        row = anchor._from.row + 1
        return f"{col}{row}"
    return "A1"
```

## 3. Theme Colors (テーマカラー)

### 課題

openpyxl の Color オブジェクトは3種類の色指定方法がある:
1. `rgb`: 直接ARGB指定 (例: "FF000000")
2. `theme`: テーマカラーインデックス (0-11) + tint
3. `indexed`: インデックスカラー (0-63)

### テーマカラーインデックス

| Index | Name | 説明 |
|-------|------|------|
| 0 | dk1 | Dark 1 (通常は黒) |
| 1 | lt1 | Light 1 (通常は白) |
| 2 | dk2 | Dark 2 |
| 3 | lt2 | Light 2 |
| 4 | accent1 | アクセント1 |
| 5 | accent2 | アクセント2 |
| 6 | accent3 | アクセント3 |
| 7 | accent4 | アクセント4 |
| 8 | accent5 | アクセント5 |
| 9 | accent6 | アクセント6 |
| 10 | hlink | ハイパーリンク |
| 11 | folHlink | 訪問済みリンク |

### テーマXML解析

```python
import xml.etree.ElementTree as ET

def parse_theme_colors(theme_xml: bytes) -> dict[int, str]:
    """テーマXMLからカラーマップを抽出"""
    root = ET.fromstring(theme_xml)
    ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

    clr_scheme = root.find('.//a:clrScheme', ns)
    color_order = ['dk1', 'lt1', 'dk2', 'lt2',
                   'accent1', 'accent2', 'accent3', 'accent4',
                   'accent5', 'accent6', 'hlink', 'folHlink']

    theme_colors = {}
    for i, name in enumerate(color_order):
        elem = clr_scheme.find(f'a:{name}', ns)
        if elem is not None:
            # srgbClr または sysClr から色を取得
            srgb = elem.find('a:srgbClr', ns)
            if srgb is not None:
                theme_colors[i] = srgb.get('val')
            else:
                sys_clr = elem.find('a:sysClr', ns)
                if sys_clr is not None:
                    theme_colors[i] = sys_clr.get('lastClr')

    return theme_colors
```

### Tint変換

```python
import colorsys

def apply_tint(rgb_hex: str, tint: float) -> str:
    """RGB色にtint変換を適用"""
    r = int(rgb_hex[0:2], 16) / 255.0
    g = int(rgb_hex[2:4], 16) / 255.0
    b = int(rgb_hex[4:6], 16) / 255.0

    h, l, s = colorsys.rgb_to_hls(r, g, b)

    if tint < 0:
        l = l * (1.0 + tint)
    else:
        l = l * (1.0 - tint) + tint

    l = max(0.0, min(1.0, l))
    r, g, b = colorsys.hls_to_rgb(h, l, s)

    return f"{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"
```

### デフォルトテーマカラー

workbook.loaded_themeがNoneの場合のフォールバック:

```python
DEFAULT_THEME_COLORS = {
    0: "000000",  # dk1
    1: "FFFFFF",  # lt1
    2: "1F497D",  # dk2
    3: "EEECE1",  # lt2
    4: "4F81BD",  # accent1
    5: "C0504D",  # accent2
    6: "9BBB59",  # accent3
    7: "8064A2",  # accent4
    8: "4BACC6",  # accent5
    9: "F79646",  # accent6
    10: "0000FF", # hlink
    11: "800080", # folHlink
}
```

## 4. 実装計画

### Phase 2 実装順序

1. **extractors/validation.py**: extract_validations() の実装
2. **extractors/image.py**: extract_images() の実装
3. **extractors/color.py**: テーマカラー解決ロジック (resolve_theme_color)
4. **extractors/cell.py**: _resolve_color() の改善（テーマカラー対応）
5. **core.py**: dump() と dump_sheet() に新機能を統合
6. **sheet.py**: has_images, has_data_validations の正確な検出
7. **テスト**: 各機能のユニットテスト作成

### 依存関係

- `pillow`: 画像処理のテスト用（既にインストール済み）
- `colorsys`: tint変換（標準ライブラリ）
- `xml.etree.ElementTree`: テーマXML解析（標準ライブラリ）

### 注意事項

1. **画像アクセス**: `ws._images` はプライベート属性だが、openpyxlでは公式にサポートされているアクセス方法
2. **テーマカラー**: workbook.loaded_theme が None の場合はデフォルト値を使用
3. **データ検証**: sqref が複数範囲を含む場合がある（例: "A1:A10 C1:C10"）
