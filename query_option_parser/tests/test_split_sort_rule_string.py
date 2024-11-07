"""Test split_sort_rule_string"""

from enums.table import CliTableColumn, SortingDirection
from query_option_parser.parser_utils import split_sort_rule_string


def test_valid_sort_string() -> None:
    """Check valid case"""
    column_name, sorting_direction = split_sort_rule_string("linecount ASC")
    assert column_name == CliTableColumn.LINE_COUNT
    assert sorting_direction == SortingDirection.ASC


def test_incorrect_column_name() -> None:
    """Check incorrect column name"""
    column_name, sorting_direction = split_sort_rule_string("random ASC")
    assert column_name is None
    assert sorting_direction == SortingDirection.ASC


def test_incorrect_sorting_direction() -> None:
    """Check incorrect column name"""
    column_name, sorting_direction = split_sort_rule_string("daratio FLAT")
    assert column_name == CliTableColumn.DELETED_ADDED_RATIO
    assert sorting_direction is None
