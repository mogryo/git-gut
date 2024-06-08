"""Test parse_order_statement"""

from enums.columns import CliTableColumn, SortingDirection
from query_option_parser.parser import parse_order_statement


def test_valid_single_sort() -> None:
    """Check single sort rule"""
    result = parse_order_statement("linecount ASC")
    assert len(result.sort_rule_nodes) == 1
    assert result.sort_rule_nodes[0].column_name == CliTableColumn.LINE_COUNT
    assert result.sort_rule_nodes[0].sort_direction == SortingDirection.ASC


def test_valid_multiple_sort() -> None:
    """Check multiple sort rules"""
    result = parse_order_statement("linecount ASC and daratio DESC")
    assert len(result.sort_rule_nodes) == 2
    assert result.sort_rule_nodes[0].column_name == CliTableColumn.LINE_COUNT
    assert result.sort_rule_nodes[0].sort_direction == SortingDirection.ASC
    assert result.sort_rule_nodes[1].column_name == CliTableColumn.DELETED_ADDED_RATIO
    assert result.sort_rule_nodes[1].sort_direction == SortingDirection.DESC


def test_invalid_column_name_multiple_sort() -> None:
    """Check when invalid column name is provided"""
    result = parse_order_statement("random ASC and daratio DESC")
    assert len(result.sort_rule_nodes) == 1
    assert result.sort_rule_nodes[0].column_name == CliTableColumn.DELETED_ADDED_RATIO
    assert result.sort_rule_nodes[0].sort_direction == SortingDirection.DESC


def test_invalid_sort_direction_multiple_sort() -> None:
    """Check when invalid sort direction is provided"""
    result = parse_order_statement("linecount ASC and daratio FLAT")
    assert len(result.sort_rule_nodes) == 1
    assert result.sort_rule_nodes[0].column_name == CliTableColumn.LINE_COUNT
    assert result.sort_rule_nodes[0].sort_direction == SortingDirection.ASC
