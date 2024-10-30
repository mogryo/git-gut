"""Validators for node statements"""

from typing import List
from pydash import every
from command_interface.help_text import COMMAND_OPTION_COLUMN_NAMES
from enums.columns import CliTableColumn, SortingDirection


def is_column_name(text: str) -> bool:
    """Check if word is column name"""
    return text in COMMAND_OPTION_COLUMN_NAMES


def are_column_names_valid(column_names: List[str]) -> bool:
    """Validate provided column names"""
    return every(column_names, is_column_name)


def is_valid_sort(
    column_name: CliTableColumn | None,
    sort_direction: SortingDirection | None,
) -> bool:
    """Check if sort is valid"""
    return isinstance(column_name, CliTableColumn) and isinstance(
        sort_direction, SortingDirection
    )
