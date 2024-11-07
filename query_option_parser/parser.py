"""Parser functions"""

import ast
from typing import List, Optional, cast
from itertools import batched

from app_types.validation_errors import NodeValidationError
from app_types.result import ResultOk, ResultValidationError, ResultUnion
from enums.application import Severity
from enums.table import CliTableColumn
from query_option_parser.nodes import (
    IntervalNode,
    ShowNode,
    OrderNode,
    SortRuleNode,
    FromNode,
    WhereNode,
)
from query_option_parser.parser_utils import (
    split_sort_rule_string,
    extract_since_and_until_interval,
)
from utils.mappings import REVERSE_COLUMN_NAME_MAPPING
from validators.statement_validators import is_column_name, is_valid_sort


def parse_where_statement(
    where_statement: Optional[str] = "",
) -> ResultUnion[WhereNode]:
    """Parse statement with Python ast module"""
    if where_statement is None or where_statement.strip() == "":
        return ResultOk(WhereNode(None))

    corrected_where_statement = (
        where_statement.replace(" AND ", " and ")
        .replace(" OR ", " or ")
        .replace(" NOT ", " not ")
    )
    try:
        parsed_ast_statement = ast.parse(
            f"""if {corrected_where_statement }: \n\tpass"""
        )
    except SyntaxError:
        return ResultValidationError(
            where_statement,
            [
                NodeValidationError(
                    corrected_where_statement,
                    "Couldn't parse condition",
                    Severity.CRITICAL,
                )
            ],
        )

    return ResultOk(
        WhereNode(cast(ast.BoolOp, cast(ast.If, parsed_ast_statement.body[0]).test))
    )


def parse_show_statement(
    show_statement: Optional[str],
) -> ResultUnion[ShowNode, NodeValidationError, None]:
    """Parse show statement"""
    string_column_names = (show_statement or "").replace(" ", "").split(",")

    validation_errors = [
        NodeValidationError(column_name, "Incorrect column name", Severity.CRITICAL)
        for column_name in string_column_names
        if not is_column_name(column_name)
    ]
    if len(validation_errors) != 0:
        return ResultValidationError(show_statement, validation_errors)

    enum_column_names: List[CliTableColumn] = []
    for column_name in string_column_names:
        enum_column_names.append(REVERSE_COLUMN_NAME_MAPPING[column_name])

    return ResultOk(ShowNode(enum_column_names))


def parse_order_statement(order_statement: Optional[str]) -> ResultUnion[OrderNode]:
    """Parse order(sort) statement"""
    parsed_order_statement = (
        (order_statement or "").replace(" AND ", " and ").split(" and ")
    )
    validation_errors = [
        NodeValidationError(sort_rule, "Incorrect sort rule", Severity.CRITICAL)
        for sort_rule in parsed_order_statement
        if not is_valid_sort(*split_sort_rule_string(sort_rule))
    ]
    if len(validation_errors) != 0:
        return ResultValidationError(order_statement, validation_errors)

    sort_rule_nodes: List[SortRuleNode] = []
    for sort_rule in parsed_order_statement:
        column_name, sort_direction = split_sort_rule_string(sort_rule)
        sort_rule_nodes.append(SortRuleNode(column_name, sort_direction))

    return ResultOk(OrderNode(sort_rule_nodes))


def parse_from_statement(from_statement: Optional[str] = "") -> ResultOk[FromNode]:
    """Parse from statement"""
    return ResultOk(FromNode(from_statement if from_statement is not None else ""))


def parse_interval_statement(
    interval_statement: Optional[str] = "",
) -> ResultUnion[IntervalNode, NodeValidationError]:
    """Parse interval statement"""
    split_words = (
        [word.upper() for word in interval_statement.split()]
        if interval_statement is not None
        else []
    )

    if not (len(split_words) == 2 or len(split_words) == 4):
        return ResultValidationError(
            interval_statement,
            [
                NodeValidationError(
                    ", ".join(split_words),
                    "Please specify correct INTERVAL",
                    Severity.CRITICAL,
                )
            ],
        )

    since: str | None = None
    until: str | None = None
    validation_errors = []

    for single_interval_words in list(batched(split_words, 2)):
        extraction_result = extract_since_and_until_interval(single_interval_words)
        match extraction_result:
            case ResultValidationError():
                validation_errors.extend(extraction_result.validation_error)
            case ResultOk():
                since, until = extraction_result.value

    if len(validation_errors) > 0:
        return ResultValidationError(interval_statement, validation_errors)

    return ResultOk(IntervalNode(since, until))


TOP_LEVEL_STATEMENT_PARSERS = {
    "SHOW": parse_show_statement,
    "FROM": parse_from_statement,
    "WHERE": parse_where_statement,
    "ORDERBY": parse_order_statement,
    "INTERVAL": parse_interval_statement,
}

ROOT_NODE_KEYS = {
    "SHOW": "show_node",
    "FROM": "from_node",
    "WHERE": "where_node",
    "ORDERBY": "order_node",
    "INTERVAL": "interval_node",
}
