"""Validators for root node"""

import sys
from typing import Any

from query_option_parser.nodes import StatementNode
from app_types.result import ResultUnion, ResultException, ResultOk


def assert_from_node_provided(root_node: StatementNode) -> None:
    """Assert that from node is provided"""
    if root_node.from_node is None:
        print("FROM path was not provided")
        sys.exit()


def assert_show_node_provided(root_node: StatementNode) -> None:
    """Assert that show node is provided"""
    if root_node.show_node is None:
        print("FROM path was not provided")
        sys.exit()


def assert_root_node_result_is_valid(
    root_node_result: ResultUnion[StatementNode, Any, Any]
) -> None:
    """Assert the root node result union is valid data"""
    match root_node_result:
        case ResultException():
            print("Exiting program due to errors in parsing the options/query")
            sys.exit()
        case ResultOk():
            assert_from_node_provided(root_node_result.value)
            assert_show_node_provided(root_node_result.value)
