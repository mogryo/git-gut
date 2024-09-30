"""Test parse_separate_options_into_query"""

from app_types.dataclasses import SeparateOptionsAsQuery
from enums.user_input_keywords import QueryKeywords
from utils.command_option_parser import parse_separate_options_into_query

COLUMNS = "linecount, daratio"
FILE_PATH = "./utils"
FILTERS = "linecount > 100 AND daratio < 10"
SORT = "linecount ASC AND daratio DESC"


def test_only_columns() -> None:
    """Check when only columns are provided"""
    result = parse_separate_options_into_query(SeparateOptionsAsQuery(columns=COLUMNS))
    assert result == f"{QueryKeywords.SHOW.value} {COLUMNS}"


def test_columns_path() -> None:
    """Check when columns and path are provided"""
    result = parse_separate_options_into_query(
        SeparateOptionsAsQuery(columns=COLUMNS, file_path=FILE_PATH)
    )
    assert (
        result
        == f"{QueryKeywords.SHOW.value} {COLUMNS} {QueryKeywords.FROM.value} {FILE_PATH}"
    )


def test_orderby_and_where() -> None:
    """Check when sort and filters are provided"""
    result = parse_separate_options_into_query(
        SeparateOptionsAsQuery(filters=FILTERS, sort=SORT)
    )
    assert (
        result
        == f"{QueryKeywords.WHERE.value} {FILTERS} {QueryKeywords.ORDERBY.value} {SORT}"
    )
