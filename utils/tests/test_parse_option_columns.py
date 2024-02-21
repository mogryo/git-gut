"""Test parse_option_columns"""
from utils import parse_option_columns
from app_types import CliTableColumn


def test_empty_string() -> None:
    """Check empty string returns empty list"""
    assert not parse_option_columns("")


def test_single_column_name() -> None:
    """Check single name in string is parsed correctly"""
    assert parse_option_columns(
        f"{CliTableColumn.FILE_NAME.value}"
    ) == [CliTableColumn.FILE_NAME.value]


def test_single_column_name_with_whitespaces_commas() -> None:
    """Check whitespaces and commas are ignore, and single name"""
    assert parse_option_columns(
        f"   {CliTableColumn.FILE_NAME.value}  , "
    ) == [CliTableColumn.FILE_NAME.value]


def test_multiple_column_names() -> None:
    """Check multiple names are parsed"""
    assert parse_option_columns(
        f"{CliTableColumn.FILE_NAME.value},{CliTableColumn.ID.value}"
    ) == [CliTableColumn.FILE_NAME.value, CliTableColumn.ID.value]


def test_multiple_column_names_with_whitespaces_commas() -> None:
    """Check whitespaces and commas are ignore, with multiple names"""
    assert parse_option_columns(
        f"  ,{CliTableColumn.FILE_NAME.value}  ,  {CliTableColumn.ID.value}  , ,"
    ) == [CliTableColumn.FILE_NAME.value, CliTableColumn.ID.value]
