"""Test is_allowed_condition"""

from enums.columns import CliTableColumn
from query_option_parser.parser import is_allowed_condition


def test_valid_condition() -> None:
    """Test valid condition"""
    assert is_allowed_condition(CliTableColumn.LINE_COUNT.value, ">", "100")


def test_invalid_column_name() -> None:
    """Test invalid column name"""
    assert not is_allowed_condition("random", ">", "100")


def test_invalid_sign() -> None:
    """Test invalid sign"""
    assert not is_allowed_condition(CliTableColumn.LINE_COUNT.value, ">=---", "100")
