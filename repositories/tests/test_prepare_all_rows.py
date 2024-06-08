"""Test prepare_all_rows"""

from enums.columns import CliTableColumn
from repositories.git_stat_repo import prepare_all_rows


def test_empty_columns_and_rows() -> None:
    """Test empty columns and rows"""
    assert not prepare_all_rows([], [])


def test_only_empty_rows() -> None:
    """Test empty rows but with columns"""
    assert not prepare_all_rows([CliTableColumn.FILE_NAME], [])


def test_only_empty_columns() -> None:
    """Test empty columns but with rows"""
    assert not prepare_all_rows([], [["data", "data"]])


def test_populated_columns_and_rows() -> None:
    """Test that both rows and columns are provided"""
    rows = prepare_all_rows(
        [CliTableColumn.MOST_ADDED_AUTHOR, CliTableColumn.COMMIT_AMOUNT],
        [["author", 10]],
    )

    assert rows[0].maauthor == "author" and rows[0].commitcount == 10
