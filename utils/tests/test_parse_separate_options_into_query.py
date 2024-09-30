"""Test parse_separate_options_into_query"""

from app_types.dataclasses import SeparateOptionsAsQuery
from enums.user_input_keywords import QueryKeywords
from utils.command_option_parser import parse_separate_options_into_query

columns = "linecount, daratio"
file_path = "./utils"
filters = "linecount > 100 AND daratio < 10"
sort = "linecount ASC AND daratio DESC"


def test_only_columns() -> None:
    """Check when only columns are provided"""
    result = parse_separate_options_into_query(SeparateOptionsAsQuery(columns=columns))
    assert result == f"{QueryKeywords.SHOW.value} {columns}"


def test_columns_path() -> None:
    """Check when columns and path are provided"""
    result = parse_separate_options_into_query(
        SeparateOptionsAsQuery(columns=columns, file_path=file_path)
    )
    assert (
        result
        == f"{QueryKeywords.SHOW.value} {columns} {QueryKeywords.FROM.value} {file_path}"
    )


def test_orderby_and_where() -> None:
    """Check when sort and filters are provided"""
    result = parse_separate_options_into_query(
        SeparateOptionsAsQuery(filters=filters, sort=sort)
    )
    assert (
        result
        == f"{QueryKeywords.WHERE.value} {filters} {QueryKeywords.ORDERBY.value} {sort}"
    )
