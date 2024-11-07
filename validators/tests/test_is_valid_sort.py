"""Test is_valid_sort"""

from enums.table import SortingDirection, CliTableColumn
from validators.statement_validators import is_valid_sort


def test_incorrect_column_name() -> None:
    """Test incorrect column name"""
    assert not is_valid_sort(None, SortingDirection.ASC)


def test_incorrect_sorting_direction() -> None:
    """Test incorrect sorting direction"""
    assert not is_valid_sort(CliTableColumn.FILE_NAME, None)


def test_valid_arguments() -> None:
    """Test valid arguments"""
    assert is_valid_sort(CliTableColumn.FILE_NAME, SortingDirection.DESC)
