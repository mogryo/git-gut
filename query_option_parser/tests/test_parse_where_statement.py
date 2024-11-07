"""Test parse_where_statement"""

import ast
from typing import cast

from app_types.validation_errors import NodeValidationError
from app_types.result import ResultValidationError
from query_option_parser.parser import parse_where_statement


def test_valid_single_condition() -> None:
    """Check valid single condition"""
    result = parse_where_statement("linecount > 100").value.condition_node
    assert isinstance(result, ast.Compare)
    assert cast(ast.Name, result.left).id == "linecount"
    assert isinstance(result.ops[0], ast.Gt)
    assert cast(ast.Constant, result.comparators[0]).value == 100


def test_valid_multiple_conditions_with_and() -> None:
    """Check multiple valid conditions, joined by and"""
    result = parse_where_statement(
        "linecount > 100 and daratio <= 9"
    ).value.condition_node
    assert isinstance(result, ast.BoolOp)
    assert isinstance(result.values[0], ast.Compare)
    assert isinstance(result.values[1], ast.Compare)
    assert isinstance(result.op, ast.And)

    assert cast(ast.Name, cast(ast.Compare, result.values[0]).left).id == "linecount"
    assert isinstance(cast(ast.Compare, result.values[0]).ops[0], ast.Gt)
    assert (
        cast(ast.Constant, cast(ast.Compare, result.values[0]).comparators[0]).value
        == 100
    )

    assert cast(ast.Name, cast(ast.Compare, result.values[1]).left).id == "daratio"
    assert isinstance(cast(ast.Compare, result.values[1]).ops[0], ast.LtE)
    assert (
        cast(ast.Constant, cast(ast.Compare, result.values[1]).comparators[0]).value
        == 9
    )


def test_valid_multiple_conditions_with_or() -> None:
    """Check multiple valid conditions, joined by or"""
    result = parse_where_statement(
        "linecount > 100 or daratio <= 9"
    ).value.condition_node
    assert isinstance(result, ast.BoolOp)
    assert isinstance(result.values[0], ast.Compare)
    assert isinstance(result.values[1], ast.Compare)
    assert isinstance(result.op, ast.Or)

    assert cast(ast.Name, cast(ast.Compare, result.values[0]).left).id == "linecount"
    assert isinstance(cast(ast.Compare, result.values[0]).ops[0], ast.Gt)
    assert (
        cast(ast.Constant, cast(ast.Compare, result.values[0]).comparators[0]).value
        == 100
    )

    assert cast(ast.Name, cast(ast.Compare, result.values[1]).left).id == "daratio"
    assert isinstance(cast(ast.Compare, result.values[1]).ops[0], ast.LtE)
    assert (
        cast(ast.Constant, cast(ast.Compare, result.values[1]).comparators[0]).value
        == 9
    )


def test_valid_nested_conditions() -> None:
    """Check multiple nested conditions"""
    result = parse_where_statement(
        "linecount > 100 and (daratio <= 9 or maauthor == 'mogryo')"
    ).value.condition_node
    assert isinstance(result, ast.BoolOp)
    assert isinstance(result.values[0], ast.Compare)
    assert isinstance(result.values[1], ast.BoolOp)
    assert isinstance(result.op, ast.And)

    assert cast(ast.Name, cast(ast.Compare, result.values[0]).left).id == "linecount"
    assert isinstance(cast(ast.Compare, result.values[0]).ops[0], ast.Gt)
    assert (
        cast(ast.Constant, cast(ast.Compare, result.values[0]).comparators[0]).value
        == 100
    )

    nested_condition = cast(ast.BoolOp, result.values[1])
    assert (
        cast(ast.Name, cast(ast.Compare, nested_condition.values[0]).left).id
        == "daratio"
    )
    assert isinstance(cast(ast.Compare, nested_condition.values[0]).ops[0], ast.LtE)
    assert (
        cast(
            ast.Constant, cast(ast.Compare, nested_condition.values[0]).comparators[0]
        ).value
        == 9
    )
    assert (
        cast(ast.Name, cast(ast.Compare, nested_condition.values[1]).left).id
        == "maauthor"
    )
    assert isinstance(cast(ast.Compare, nested_condition.values[1]).ops[0], ast.Eq)
    assert (
        cast(
            ast.Constant, cast(ast.Compare, nested_condition.values[1]).comparators[0]
        ).value
        == "mogryo"
    )


def test_empty_condition() -> None:
    """Check empty condition"""
    result = parse_where_statement()
    assert result.value.condition_node is None


def test_invalid_conditions_raise_syntax_error() -> None:
    """Check invalid conditions raise syntax error"""
    result = parse_where_statement("linecount > 100 and daratio <== d9")
    assert isinstance(result, ResultValidationError)
    assert len(result.validation_error) == 1
    assert isinstance(result.validation_error[0], NodeValidationError)


def test_lower_upper_case_or() -> None:
    """Check lower and upper case for operator or"""
    result = parse_where_statement(
        "linecount > 100 or daratio <= 9"
    ).value.condition_node
    assert isinstance(result, ast.BoolOp)
    assert isinstance(result.values[0], ast.Compare)
    assert isinstance(result.values[1], ast.Compare)
    assert isinstance(result.op, ast.Or)

    result = parse_where_statement(
        "linecount > 100 OR daratio <= 9"
    ).value.condition_node
    assert isinstance(result, ast.BoolOp)
    assert isinstance(result.values[0], ast.Compare)
    assert isinstance(result.values[1], ast.Compare)
    assert isinstance(result.op, ast.Or)


def test_lower_upper_case_and() -> None:
    """Check lower and upper case for operator and"""
    result = parse_where_statement(
        "linecount > 100 and daratio <= 9"
    ).value.condition_node
    assert isinstance(result, ast.BoolOp)
    assert isinstance(result.values[0], ast.Compare)
    assert isinstance(result.values[1], ast.Compare)
    assert isinstance(result.op, ast.And)

    result = parse_where_statement(
        "linecount > 100 AND daratio <= 9"
    ).value.condition_node
    assert isinstance(result, ast.BoolOp)
    assert isinstance(result.values[0], ast.Compare)
    assert isinstance(result.values[1], ast.Compare)
    assert isinstance(result.op, ast.And)
