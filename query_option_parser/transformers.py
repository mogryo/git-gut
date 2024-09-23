"""Transform nodes into sqlalchemy objects, queries, statements"""

import ast
from typing import List, cast
from sqlalchemy import and_, or_, asc, desc, UnaryExpression

from enums.columns import SortingDirection, CliTableColumn
from orm.git_stat import GitStat
from query_option_parser.nodes import SortRuleNode, ShowNode
from utils.git_utils import get_top_author_by_stat


def map_sign_to_filter(compare: ast.Compare):
    """Map condition to filter, depending on sign"""
    left = cast(ast.Name, compare.left)
    orm_field = getattr(GitStat, left.id)
    literal = cast(ast.Constant, compare.comparators[0]).value

    match compare.ops[0]:
        case ast.Gt():
            return orm_field > literal
        case ast.GtE():
            return orm_field >= literal
        case ast.Lt():
            return orm_field < literal
        case ast.LtE():
            return orm_field <= literal
        case ast.Eq():
            return orm_field == literal
        case ast.NotEq():
            return orm_field != literal


def map_bool_operation_to_orm_operation(bool_operation: ast.BoolOp):
    """Map Python BoolOp operation, to ORM logical operation"""
    if not hasattr(bool_operation, "op"):
        return or_

    match bool_operation.op:
        case ast.And():
            return and_
        case ast.Or():
            return or_


def transform_ast_bool_op_to_orm_filters(test_statement: ast.BoolOp | ast.Compare):
    """Transform Python AST bool operation to ORM filters"""
    if isinstance(test_statement, ast.Compare):
        return map_sign_to_filter(test_statement)

    logical_operator = map_bool_operation_to_orm_operation(test_statement)
    if logical_operator is None:
        print("Filter bool operator is not supported")
        exit()

    binary_conditions = []
    for single_value in test_statement.values:
        if isinstance(single_value, ast.Compare):
            compare_statement = map_sign_to_filter(single_value)
            binary_conditions.append(compare_statement)
        elif isinstance(single_value, ast.BoolOp):
            binary_conditions.append(transform_ast_bool_op_to_orm_filters(single_value))

    return logical_operator(*binary_conditions)


COLUMN_TO_GIT_STAT_MAPPING = {
    column.value: getattr(GitStat, column.value) for column in CliTableColumn
}


def transform_sort_nodes_to_order_by(
    sort_rule_nodes: List[SortRuleNode],
) -> List[UnaryExpression]:
    """Transform all sort rule nodes to order by"""
    order_by_list = []
    for rule_node in sort_rule_nodes:
        order_direction = (
            asc if rule_node.sort_direction == SortingDirection.ASC else desc
        )
        order_by_list.append(
            order_direction(COLUMN_TO_GIT_STAT_MAPPING[rule_node.column_name.value]),
        )

    return order_by_list


def transform_show_node_to_select(show_node: ShowNode):
    """Transform show node to list of GitStat orm fields"""
    git_stat_columns = []
    for column_name in show_node.column_names:
        git_stat_columns.append(COLUMN_TO_GIT_STAT_MAPPING[column_name.value])

    return git_stat_columns
