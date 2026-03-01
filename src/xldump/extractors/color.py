"""Color resolution utilities.

This module provides functions to resolve openpyxl Color objects to
ARGB hex strings, including theme color resolution.
"""

from __future__ import annotations

import colorsys
from typing import TYPE_CHECKING, Any
import xml.etree.ElementTree as ET

if TYPE_CHECKING:
    from openpyxl.styles.colors import Color
    from openpyxl.workbook import Workbook

# Default Office theme colors (used when workbook theme is not available)
DEFAULT_THEME_COLORS: dict[int, str] = {
    0: "000000",  # dk1 (Dark 1 - usually black)
    1: "FFFFFF",  # lt1 (Light 1 - usually white)
    2: "1F497D",  # dk2 (Dark 2)
    3: "EEECE1",  # lt2 (Light 2)
    4: "4F81BD",  # accent1
    5: "C0504D",  # accent2
    6: "9BBB59",  # accent3
    7: "8064A2",  # accent4
    8: "4BACC6",  # accent5
    9: "F79646",  # accent6
    10: "0000FF",  # hlink
    11: "800080",  # folHlink
}

# Standard indexed colors (first 8, commonly used)
INDEXED_COLORS: dict[int, str] = {
    0: "000000",  # Black
    1: "FFFFFF",  # White
    2: "FF0000",  # Red
    3: "00FF00",  # Green
    4: "0000FF",  # Blue
    5: "FFFF00",  # Yellow
    6: "FF00FF",  # Magenta
    7: "00FFFF",  # Cyan
}


def resolve_color(color: Color | None, workbook: Workbook | None = None) -> str | None:
    """Resolve an openpyxl Color object to an ARGB hex string.

    Handles rgb, theme, and indexed color types.

    Args:
        color: The openpyxl Color object to resolve.
        workbook: The workbook for theme color resolution (optional).

    Returns:
        The ARGB hex string (e.g., "FF000000") or None if unresolvable.

    """
    if color is None:
        return None

    # Handle direct RGB color
    if color.type == "rgb" and color.rgb:
        rgb = color.rgb
        if isinstance(rgb, str):
            # Handle both 6-digit and 8-digit hex
            if len(rgb) == 6:
                return f"FF{rgb}"
            return rgb
        return None

    # Handle theme color
    if color.type == "theme" and color.theme is not None:
        return _resolve_theme_color(color, workbook)

    # Handle indexed color
    if color.type == "indexed" and color.indexed is not None:
        indexed_rgb = INDEXED_COLORS.get(color.indexed)
        if indexed_rgb:
            return f"FF{indexed_rgb}"
        return None

    # Fallback: try to get rgb directly
    if hasattr(color, "rgb") and color.rgb:
        try:
            rgb = str(color.rgb)
            if len(rgb) == 6:
                return f"FF{rgb}"
            elif len(rgb) == 8:
                return rgb
        except (ValueError, TypeError):
            pass

    return None


def _resolve_theme_color(color: Color, workbook: Workbook | None) -> str | None:
    """Resolve a theme color to an ARGB hex string.

    Args:
        color: The Color object with type='theme'.
        workbook: The workbook containing theme information.

    Returns:
        The ARGB hex string or None if unresolvable.

    """
    theme_index = color.theme
    tint = color.tint if color.tint else 0.0

    # Get base color from theme
    base_rgb = _get_theme_base_color(theme_index, workbook)
    if not base_rgb:
        return None

    # Apply tint if needed
    if tint != 0.0:
        base_rgb = _apply_tint(base_rgb, tint)

    return f"FF{base_rgb}"


def _get_theme_base_color(theme_index: int, workbook: Workbook | None) -> str | None:
    """Get the base RGB color for a theme color index.

    Args:
        theme_index: The theme color index (0-11).
        workbook: The workbook containing theme information.

    Returns:
        The RGB hex string (6 characters) or None if unresolvable.

    """
    # Try to parse from workbook theme
    if workbook and workbook.loaded_theme:
        theme_colors = _parse_theme_colors(workbook.loaded_theme)
        if theme_index in theme_colors:
            return theme_colors[theme_index]

    # Fall back to default theme colors
    return DEFAULT_THEME_COLORS.get(theme_index)


def _parse_theme_colors(theme_xml: bytes) -> dict[int, str]:
    """Parse theme colors from theme XML.

    Args:
        theme_xml: The raw theme XML bytes.

    Returns:
        A dict mapping theme index to RGB hex string.

    """
    try:
        # The theme_xml is trusted data from openpyxl's internal parsing
        root = ET.fromstring(theme_xml)  # noqa: S314
    except ET.ParseError:
        return {}

    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}

    clr_scheme = root.find(".//a:clrScheme", ns)
    if clr_scheme is None:
        return {}

    color_order = [
        "dk1",
        "lt1",
        "dk2",
        "lt2",
        "accent1",
        "accent2",
        "accent3",
        "accent4",
        "accent5",
        "accent6",
        "hlink",
        "folHlink",
    ]

    theme_colors: dict[int, str] = {}
    for i, name in enumerate(color_order):
        elem = clr_scheme.find(f"a:{name}", ns)
        if elem is not None:
            # Check for srgbClr (direct RGB)
            srgb = elem.find("a:srgbClr", ns)
            if srgb is not None:
                val = srgb.get("val")
                if val:
                    theme_colors[i] = val
                continue

            # Check for sysClr (system color with lastClr)
            sys_clr = elem.find("a:sysClr", ns)
            if sys_clr is not None:
                last_clr = sys_clr.get("lastClr")
                if last_clr:
                    theme_colors[i] = last_clr

    return theme_colors


def _apply_tint(rgb_hex: str, tint: float) -> str:
    """Apply tint transformation to RGB color.

    Args:
        rgb_hex: The RGB hex string (6 characters).
        tint: The tint value (-1.0 to 1.0). Positive = lighter, negative = darker.

    Returns:
        The transformed RGB hex string (6 characters).

    """
    # Parse RGB
    r = int(rgb_hex[0:2], 16) / 255.0
    g = int(rgb_hex[2:4], 16) / 255.0
    b = int(rgb_hex[4:6], 16) / 255.0

    # Convert to HLS
    h, l_val, s = colorsys.rgb_to_hls(r, g, b)

    # Apply tint using ECMA-376 formula
    if tint < 0:  # noqa: SIM108 (keep if-else for readability with comments)
        # Darker: L' = L * (1 + tint)
        l_val = l_val * (1.0 + tint)
    else:
        # Lighter: L' = L * (1 - tint) + tint
        l_val = l_val * (1.0 - tint) + tint

    # Clamp luminance
    l_val = max(0.0, min(1.0, l_val))

    # Convert back to RGB
    r, g, b = colorsys.hls_to_rgb(h, l_val, s)

    # Convert to hex
    return f"{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"


def get_color_cache_key(color: Any) -> str | None:
    """Generate a cache key for a color object.

    Args:
        color: The color object.

    Returns:
        A string key for caching, or None if the color is None.

    """
    if color is None:
        return None

    if hasattr(color, "type"):
        if color.type == "rgb":
            return f"rgb:{color.rgb}"
        elif color.type == "theme":
            return f"theme:{color.theme}:{color.tint}"
        elif color.type == "indexed":
            return f"indexed:{color.indexed}"

    return None
