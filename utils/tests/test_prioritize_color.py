"""Test prioritize_color"""

from enums.table import AvailableTableRowColors
from utils.colors import prioritize_color


def test_prioritize_color_two_equal() -> None:
    """Check when both colors are equal"""
    assert (
        prioritize_color(AvailableTableRowColors.GREEN, AvailableTableRowColors.GREEN)
        == AvailableTableRowColors.GREEN
    )


def test_prioritize_color_green_and_yellow() -> None:
    """Check green and yellow colors"""
    assert (
        prioritize_color(AvailableTableRowColors.YELLOW, AvailableTableRowColors.GREEN)
        == AvailableTableRowColors.YELLOW
    )


def test_prioritize_color_green_and_red() -> None:
    """Check green and red colors"""
    assert (
        prioritize_color(AvailableTableRowColors.RED, AvailableTableRowColors.GREEN)
        == AvailableTableRowColors.RED
    )


def test_prioritize_color_red_and_yellow() -> None:
    """Check red and yellow colors"""
    assert (
        prioritize_color(AvailableTableRowColors.RED, AvailableTableRowColors.YELLOW)
        == AvailableTableRowColors.RED
    )
