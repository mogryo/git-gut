"""Test parse_show_statement"""
from enums.columns import CliTableColumn
from query_option_parser.parser import parse_show_statement


def test_valid_columns() -> None:
    """Check valid columns"""
    result = parse_show_statement("linecount, daratio")
    assert len(result.column_names) == 2
    assert result.column_names[0] == CliTableColumn.LINE_COUNT
    assert result.column_names[1] == CliTableColumn.DELETED_ADDED_RATIO


def test_invalid_one_column_in_multiple() -> None:
    """Check that single incorrect column is ignored, when multiple are provided"""
    result = parse_show_statement("linecount, random")
    assert len(result.column_names) == 1
    assert result.column_names[0] == CliTableColumn.LINE_COUNT


def test_invalid_all_columns_in_multiple() -> None:
    """Check that all incorrect columns are ignored, when multiple are provided"""
    result = parse_show_statement("randomOne, randomTwo")
    assert len(result.column_names) == 0
