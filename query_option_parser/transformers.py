"""Transform nodes into sqlalchemy objects, queries, statements"""
from typing import List
from sqlalchemy import and_

from orm.git_stat import GitStat
from query_option_parser.nodes import ConditionNode


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


def transform_condition_nodes_to_filters(condition_nodes: List[ConditionNode]):
    """Transform all condition nodes to filters, joined by and"""
    return and_(*[map_sign_to_filter(condition_node) for condition_node in condition_nodes])
