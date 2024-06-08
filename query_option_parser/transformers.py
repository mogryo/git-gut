"""Transform nodes into sqlalchemy objects, queries, statements"""

from typing import List
from sqlalchemy import and_, ColumnElement, asc, desc, UnaryExpression

from enums.columns import SortingDirection, CliTableColumn
from orm.git_stat import GitStat
from query_option_parser.nodes import ConditionNode, SortRuleNode, ShowNode


def map_sign_to_filter(condition_node: ConditionNode):
    """Map condition to filter, depending on sign"""
    orm_field = getattr(GitStat, condition_node.column_name)
    match condition_node.sign:
        case ">":
            return orm_field > condition_node.constant_part
        case ">=":
            return orm_field >= condition_node.constant_part
        case "<":
            return orm_field < condition_node.constant_part
        case "<=":
            return orm_field <= condition_node.constant_part
        case "=":
            return orm_field == condition_node.constant_part


def transform_condition_nodes_to_filters(
    condition_nodes: List[ConditionNode],
) -> ColumnElement[bool]:
    """Transform all condition nodes to filters, joined by and"""
    return and_(
        *[map_sign_to_filter(condition_node) for condition_node in condition_nodes]
    )


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
