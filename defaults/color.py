"""Defaults for column colors"""
from app_types.builders import NumberColumnColorCondition
from enums.columns import CliTableColumnColor

line_count_color = [
    NumberColumnColorCondition(0, 250, CliTableColumnColor.GREEN),
    NumberColumnColorCondition(250, 400, CliTableColumnColor.YELLOW),
    NumberColumnColorCondition(400, None, CliTableColumnColor.RED),
]

delete_add_ratio_color = [
    NumberColumnColorCondition(0, 0.15, CliTableColumnColor.GREEN),
    NumberColumnColorCondition(0.15, 0.3, CliTableColumnColor.YELLOW),
    NumberColumnColorCondition(0.3, None, CliTableColumnColor.RED),
]
