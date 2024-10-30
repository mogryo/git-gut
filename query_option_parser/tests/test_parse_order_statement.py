"""Test parse_order_statement"""

from app_types.node_validation_errors import NodeValidationError
from app_types.result import ResultValidationError
from enums.columns import CliTableColumn, SortingDirection
from query_option_parser.parser import parse_order_statement


def test_valid_single_sort() -> None:
    """Check single sort rule"""
    result = parse_order_statement("linecount ASC").value
    assert len(result.sort_rule_nodes) == 1
    assert result.sort_rule_nodes[0].column_name == CliTableColumn.LINE_COUNT
    assert result.sort_rule_nodes[0].sort_direction == SortingDirection.ASC


def test_valid_multiple_sort() -> None:
    """Check multiple sort rules"""
    result = parse_order_statement("linecount ASC and daratio DESC").value
    assert len(result.sort_rule_nodes) == 2
    assert result.sort_rule_nodes[0].column_name == CliTableColumn.LINE_COUNT
    assert result.sort_rule_nodes[0].sort_direction == SortingDirection.ASC
    assert result.sort_rule_nodes[1].column_name == CliTableColumn.DELETED_ADDED_RATIO
    assert result.sort_rule_nodes[1].sort_direction == SortingDirection.DESC


def test_invalid_column_name_multiple_sort() -> None:
    """Check when invalid column name is provided"""
    result = parse_order_statement("random ASC and daratio DESC")
    assert isinstance(result, ResultValidationError)
    assert len(result.validation_error) == 1
    assert isinstance(result.validation_error[0], NodeValidationError)


def test_invalid_sort_direction_multiple_sort() -> None:
    """Check when invalid sort direction is provided"""
    result = parse_order_statement("linecount ASC and daratio FLAT")
    assert isinstance(result, ResultValidationError)
    assert len(result.validation_error) == 1
    assert isinstance(result.validation_error[0], NodeValidationError)


def test_lower_uppercase_asc() -> None:
    """Check when asc is lower/upper case"""
    result = parse_order_statement("linecount asc").value
    assert len(result.sort_rule_nodes) == 1
    assert result.sort_rule_nodes[0].column_name == CliTableColumn.LINE_COUNT
    assert result.sort_rule_nodes[0].sort_direction == SortingDirection.ASC

    result = parse_order_statement("linecount ASC").value
    assert len(result.sort_rule_nodes) == 1
    assert result.sort_rule_nodes[0].column_name == CliTableColumn.LINE_COUNT
    assert result.sort_rule_nodes[0].sort_direction == SortingDirection.ASC


def test_lower_uppercase_desc() -> None:
    """Check when desc is lower/upper case"""
    result = parse_order_statement("linecount desc").value
    assert len(result.sort_rule_nodes) == 1
    assert result.sort_rule_nodes[0].column_name == CliTableColumn.LINE_COUNT
    assert result.sort_rule_nodes[0].sort_direction == SortingDirection.DESC

    result = parse_order_statement("linecount DESC").value
    assert len(result.sort_rule_nodes) == 1
    assert result.sort_rule_nodes[0].column_name == CliTableColumn.LINE_COUNT
    assert result.sort_rule_nodes[0].sort_direction == SortingDirection.DESC
