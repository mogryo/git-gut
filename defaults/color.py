"""Defaults for column colors"""
from app_types.dataclasses import NumberColumnColorCondition
from enums.columns import CliTableColumnColor

LINE_COUNT_COLOR = [
    NumberColumnColorCondition(0, 250, CliTableColumnColor.GREEN),
    NumberColumnColorCondition(250, 400, CliTableColumnColor.YELLOW),
    NumberColumnColorCondition(400, None, CliTableColumnColor.RED),
]

DELETE_ADD_RATIO_COLOR = [
    NumberColumnColorCondition(0, 0.15, CliTableColumnColor.GREEN),
    NumberColumnColorCondition(0.15, 0.3, CliTableColumnColor.YELLOW),
    NumberColumnColorCondition(0.3, None, CliTableColumnColor.RED),
]
