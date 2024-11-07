"""Utilities to mutate, query GitStat orm"""

from typing import List, Any
from sqlalchemy import select, Select, asc, desc
from enums.table import CliTableColumn, SortingDirection
from orm.git_stat import GitStat
from app_types.dataclasses import SortingRule
from query_option_parser.nodes import WhereNode, OrderNode, StatementNode, ShowNode
from query_option_parser.transformers import (
    transform_ast_bool_op_to_orm_filters,
    transform_sort_nodes_to_order_by,
    transform_show_node_to_select,
)


def prepare_all_rows(
    column_names: List[CliTableColumn], rows: List[List[Any]]
) -> List[GitStat]:
    """Prepare rows into GitStat ORM"""
    if len(column_names) == 0:
        return []

    git_stats = []
    for row in rows:
        data_for_git_stat = {}
        for index, column_name in enumerate(column_names):
            data_for_git_stat[column_name.value] = row[index]
        git_stats.append(GitStat(**data_for_git_stat))

    return git_stats


COLUMN_TO_GIT_STAT_MAPPING = {
    column.value: getattr(GitStat, column.value) for column in CliTableColumn
}


def prepare_select(column_names: List[CliTableColumn]) -> Select:
    """Prepare select statement for specified columns"""
    git_stat_columns = []
    for column_name in column_names:
        git_stat_columns.append(COLUMN_TO_GIT_STAT_MAPPING[column_name.value])

    return select(*git_stat_columns)


def prepare_select_from_node(show_node: ShowNode) -> Select:
    """Prepare select statement for specified columns"""
    return select(*transform_show_node_to_select(show_node))


def prepare_order_by(
    sorting_rules: List[SortingRule], select_statement: Select
) -> Select:
    """Add sorting to select statement"""
    order_by_list = []
    for rule in sorting_rules:
        order_direction = asc if rule.sort_direction == SortingDirection.ASC else desc
        order_by_list.append(
            order_direction(COLUMN_TO_GIT_STAT_MAPPING[rule.column_name.value])
        )

    return select_statement.order_by(*order_by_list)


def prepare_where(where_node: WhereNode | None, select_statement: Select) -> Select:
    """Add filtering to select statement"""
    if where_node is not None and where_node.condition_node is not None:
        return select_statement.where(
            transform_ast_bool_op_to_orm_filters(where_node.condition_node)
        )

    return select_statement


def prepare_order_by_from_node(
    orderby_node: OrderNode | None, select_statement: Select
) -> Select:
    """Add sorting to select statement"""
    if orderby_node is not None and len(orderby_node.sort_rule_nodes) > 0:
        return select_statement.order_by(
            *transform_sort_nodes_to_order_by(orderby_node.sort_rule_nodes)
        )

    return select_statement


def prepare_query_statement(root_node: StatementNode) -> Select:
    """Prepare query statement"""
    select_statement = prepare_select_from_node(root_node.show_node)
    select_statement = prepare_where(root_node.where_node, select_statement)
    select_statement = prepare_order_by_from_node(
        root_node.order_node, select_statement
    )

    return select_statement
