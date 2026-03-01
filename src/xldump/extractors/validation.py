"""Data validation extraction utilities.

This module provides functions to extract data validation rules from
openpyxl worksheets.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from xldump.models import DataValidationInfo

if TYPE_CHECKING:
    from openpyxl.worksheet.worksheet import Worksheet


def extract_validations(ws: Worksheet) -> list[DataValidationInfo]:
    """Extract all data validation rules from a worksheet.

    Args:
        ws: The openpyxl Worksheet to extract from.

    Returns:
        A list of DataValidationInfo objects representing all validation rules.

    """
    validations: list[DataValidationInfo] = []

    # Access data validations through the dataValidation attribute
    for dv in ws.data_validations.dataValidation:
        validation = DataValidationInfo(
            range=str(dv.sqref),
            type=dv.type,
            formula1=dv.formula1,
            formula2=dv.formula2,
            allow_blank=dv.allow_blank if dv.allow_blank is not None else True,
            prompt=dv.prompt,
            error=dv.error,
        )
        validations.append(validation)

    return validations


def has_data_validations(ws: Worksheet) -> bool:
    """Check if a worksheet has any data validation rules.

    Args:
        ws: The openpyxl Worksheet to check.

    Returns:
        True if the worksheet has data validations, False otherwise.

    """
    return len(ws.data_validations.dataValidation) > 0
