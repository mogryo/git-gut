from utils import parse_option_columns
from app_types import CliTableColumn


def test_empty_string() -> None:
    assert parse_option_columns("") == []


def test_single_column_name() -> None:
    assert parse_option_columns(f"{CliTableColumn.FILE_NAME.value}") == [CliTableColumn.FILE_NAME.value]


def test_single_column_name_with_whitespaces_commas() -> None:
    assert parse_option_columns(f"   {CliTableColumn.FILE_NAME.value}  , ") == [CliTableColumn.FILE_NAME.value]


def test_multiple_column_names() -> None:
    assert parse_option_columns(
        f"{CliTableColumn.FILE_NAME.value},{CliTableColumn.ID.value}"
    ) == [CliTableColumn.FILE_NAME.value, CliTableColumn.ID.value]


def test_multiple_column_names_with_whitespaces_commas() -> None:
    assert parse_option_columns(
        f"  ,{CliTableColumn.FILE_NAME.value}  ,  {CliTableColumn.ID.value}  , ,"
    ) == [CliTableColumn.FILE_NAME.value, CliTableColumn.ID.value]
