"""Test parse_option_sort"""

from utils.command_option_parser import parse_option_sort
from enums.columns import CliTableColumn, SortingDirection


def test_empty_string():
    """Check empty string returns empty list"""
    assert not parse_option_sort("")


def test_single_sort_rule():
    """Check single rule is parsed correctly"""
    sorting_rules = parse_option_sort(
        f"{CliTableColumn.FILE_NAME.value}-{SortingDirection.DESC.value}"
    )
    assert sorting_rules[0].sort_direction == SortingDirection.DESC
    assert sorting_rules[0].column_name == CliTableColumn.FILE_NAME


def test_single_sort_rule_with_whitespace_commas() -> None:
    """Check whitespaces and commas are ignore, and single sort rule"""
    sorting_rules = parse_option_sort(
        f"   {CliTableColumn.FILE_NAME.value}-{SortingDirection.DESC.value}   , "
    )
    assert sorting_rules[0].sort_direction == SortingDirection.DESC
    assert sorting_rules[0].column_name == CliTableColumn.FILE_NAME


def test_multiple_sort_rules() -> None:
    """Check multiple sort rules"""
    first_rule = f"{CliTableColumn.FILE_NAME.value}-{SortingDirection.DESC.value}"
    second_rule = f"{CliTableColumn.LINE_COUNT.value}-{SortingDirection.ASC.value}"
    sorting_rules = parse_option_sort(f"{first_rule},{second_rule}")
    assert sorting_rules[0].sort_direction == SortingDirection.DESC
    assert sorting_rules[0].column_name == CliTableColumn.FILE_NAME
    assert sorting_rules[1].sort_direction == SortingDirection.ASC
    assert sorting_rules[1].column_name == CliTableColumn.LINE_COUNT


def test_multiple_sort_rules_with_whitespaces_commas() -> None:
    """Check multiple sort rules with whitespaces and commas"""
    first_rule = f"{CliTableColumn.FILE_NAME.value}-{SortingDirection.DESC.value}"
    second_rule = f"{CliTableColumn.LINE_COUNT.value}-{SortingDirection.ASC.value}"
    sorting_rules = parse_option_sort(f"   {first_rule}  ,  {second_rule} ")
    assert sorting_rules[0].sort_direction == SortingDirection.DESC
    assert sorting_rules[0].column_name == CliTableColumn.FILE_NAME
    assert sorting_rules[1].sort_direction == SortingDirection.ASC
    assert sorting_rules[1].column_name == CliTableColumn.LINE_COUNT
