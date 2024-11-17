"""Colors logic/functions"""

from typing import TypedDict, Tuple, Optional

from enums.table import AvailableTableRowColors


class ColorRanges(TypedDict):
    """Dict to define ranges for colors"""

    green: Tuple[Optional[float | None], Optional[float | None]] | None
    yellow: Tuple[Optional[float | None], Optional[float | None]] | None
    red: Tuple[Optional[float | None], Optional[float | None]] | None


def _is_color_in_range(
    value: float,
    color_range: Tuple[Optional[float | None], Optional[float | None]] | None,
) -> bool:
    """Check if value is in range"""
    if color_range is None:
        return False

    if (
        color_range[0] is not None
        and len(color_range) == 2
        and color_range[1] is not None
    ):
        if color_range[0] <= value < color_range[1]:
            return True

    if color_range[0] is not None and (len(color_range) == 1 or color_range[1] is None):
        if color_range[0] <= value:
            return True

    if color_range[0] is None and color_range[1] is not None:
        if value < color_range[1]:
            return True

    return False


def get_color(value: float, color_dict: ColorRanges) -> AvailableTableRowColors | None:
    """Calculate color"""
    if _is_color_in_range(value, color_dict.get("green")):
        return AvailableTableRowColors.GREEN
    if _is_color_in_range(value, color_dict.get("yellow")):
        return AvailableTableRowColors.YELLOW
    if _is_color_in_range(value, color_dict.get("red")):
        return AvailableTableRowColors.RED

    return None


def prioritize_color(
    value1: AvailableTableRowColors | None, value2: AvailableTableRowColors | None
) -> AvailableTableRowColors | None:
    """From two colors pick one with more important priority (red > yellow > green)"""
    if AvailableTableRowColors.RED in (value1, value2):
        return AvailableTableRowColors.RED

    if AvailableTableRowColors.YELLOW in (value1, value2):
        return AvailableTableRowColors.YELLOW

    if AvailableTableRowColors.GREEN in (value1, value2):
        return AvailableTableRowColors.GREEN

    return None
