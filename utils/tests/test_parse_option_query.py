"""Test parse_root_statement"""
from enums.columns import CliTableColumn, SortingDirection
from utils.command_option_parser import parse_option_query


def test_only_show_statement() -> None:
    """Check when only show column statement is present"""
    result = parse_option_query("SHOW linecount, daratio")
    assert len(result.show_node.column_names) == 2
    assert result.from_node is None
    assert result.order_node is None
    assert result.where_node is None


def test_only_from_statement() -> None:
    """Check when only from statement is present"""
    result = parse_option_query("FROM ./")
    assert result.show_node is None
    assert result.from_node.path == './'
    assert result.order_node is None
    assert result.where_node is None


def test_only_order_statement() -> None:
    """Check when only order (sort) statement is present"""
    result = parse_option_query("ORDERBY daratio ASC and linecount DESC")
    assert result.show_node is None
    assert result.from_node is None
    assert len(result.order_node.sort_rule_nodes) == 2
    assert result.order_node.sort_rule_nodes[0].column_name == CliTableColumn.DELETED_ADDED_RATIO
    assert result.order_node.sort_rule_nodes[0].sort_direction == SortingDirection.ASC
    assert result.order_node.sort_rule_nodes[1].column_name == CliTableColumn.LINE_COUNT
    assert result.order_node.sort_rule_nodes[1].sort_direction == SortingDirection.DESC
    assert result.where_node is None


def test_only_where_statement() -> None:
    """Check when only where statement is present"""
    result = parse_option_query("WHERE linecount > 0 and daratio > 0.5")
    assert result.show_node is None
    assert result.from_node is None
    assert result.order_node is None
    assert len(result.where_node.condition_nodes) == 2
    assert result.where_node.condition_nodes[0].column_name == CliTableColumn.LINE_COUNT.value
    assert result.where_node.condition_nodes[0].sign == ">"
    assert result.where_node.condition_nodes[0].constant_part == 0
    assert result.where_node.condition_nodes[1]\
        .column_name == CliTableColumn.DELETED_ADDED_RATIO.value
    assert result.where_node.condition_nodes[1].sign == ">"
    assert result.where_node.condition_nodes[1].constant_part == 0.5


def test_full_valid_statement() -> None:
    """Check full statement"""
    result = parse_option_query(
        "SHOW linecount, daratio FROM ./ WHERE linecount > 100 and daratio < 1"
        " ORDERBY daratio ASC and linecount DESC"
    )
    assert len(result.show_node.column_names) == 2
    assert result.from_node.path == './'
    assert len(result.where_node.condition_nodes) == 2
    assert len(result.order_node.sort_rule_nodes) == 2
