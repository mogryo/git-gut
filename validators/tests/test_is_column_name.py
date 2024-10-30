"""Test is_column_name"""

from enums.columns import CliTableColumn
from validators.statement_validators import is_column_name


def test_column_name_is_detected() -> None:
    """Test valid column name string is acceptable"""
    assert is_column_name(CliTableColumn.LINE_COUNT.value)


def test_incorrect_name() -> None:
    """Test incorrect name"""
    assert not is_column_name("random")
