"""Test parse_where_statement"""
from query_option_parser.nodes import ConditionNode
from query_option_parser.parser import parse_where_statement


def test_valid_single_condition() -> None:
    """Check valid single condition"""
    result = parse_where_statement("linecount > 100")
    assert len(result) == 1
    assert isinstance(result[0], ConditionNode)
    assert result[0].column_name == "linecount"
    assert result[0].sign == ">"
    assert result[0].constant_part == 100


def test_valid_multiple_conditions() -> None:
    """Check multiple valid conditions"""
    result = parse_where_statement("linecount > 100 and daratio <= 9")
    assert len(result) == 2
    assert isinstance(result[0], ConditionNode)
    assert isinstance(result[1], ConditionNode)
    assert result[0].column_name == "linecount"
    assert result[0].sign == ">"
    assert result[0].constant_part == 100
    assert result[1].column_name == "daratio"
    assert result[1].sign == "<="
    assert result[1].constant_part == 9


def test_invalid_conditions_are_ignored() -> None:
    """Check invalid conditions are ignored"""
    result = parse_where_statement("linecount > 100 and darat2io<= d9")
    assert len(result) == 1
    assert isinstance(result[0], ConditionNode)
    assert result[0].column_name == "linecount"
    assert result[0].sign == ">"
    assert result[0].constant_part == 100
