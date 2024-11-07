"""Test parse_show_statement"""

from app_types.validation_errors import NodeValidationError
from app_types.result import ResultValidationError
from enums.table import CliTableColumn
from query_option_parser.parser import parse_show_statement


def test_valid_columns() -> None:
    """Check valid columns"""
    result = parse_show_statement("linecount, daratio").value
    assert len(result.column_names) == 2
    assert result.column_names[0] == CliTableColumn.LINE_COUNT
    assert result.column_names[1] == CliTableColumn.DELETED_ADDED_RATIO


def test_invalid_one_column_in_multiple() -> None:
    """Check single incorrect column is provided"""
    result = parse_show_statement("linecount, random")
    assert isinstance(result, ResultValidationError)
    assert len(result.validation_error) == 1
    assert isinstance(result.validation_error[0], NodeValidationError)


def test_invalid_all_columns_in_multiple() -> None:
    """Check multiple incorrect columns are provided"""
    result = parse_show_statement("randomOne, randomTwo")
    assert isinstance(result, ResultValidationError)
    assert len(result.validation_error) == 2
    assert isinstance(result.validation_error[0], NodeValidationError)
    assert isinstance(result.validation_error[1], NodeValidationError)
