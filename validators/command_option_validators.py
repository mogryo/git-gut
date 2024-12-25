"""Command option validators"""

import sys
from typing import Dict, List
from pydash import is_empty

from app_types.protocols import CliTable
from app_types.result import ResultValidationError, ResultUnion
from app_types.validation_errors import InvalidTableLibraryError


def assert_correct_table_library(
    table_lib_result: ResultUnion[CliTable, InvalidTableLibraryError]
) -> None:
    """Assert that table list result is successful"""
    match table_lib_result:
        case ResultValidationError():
            for error in table_lib_result.validation_error:
                print(error.message)
            sys.exit()


def assert_query_exists_for_execution(query_name: str, queries: Dict[str, str]) -> None:
    """Assert that query exists for execution"""
    if query_name not in queries:
        print(f"Cannot execute query. There is no stored query with name: {query_name}")
        sys.exit()


def assert_only_single_terminating_option_provided(
    **kwargs,
) -> None:
    """Assert only single terminating option was provided"""
    validation_messages: List[str] = []
    if kwargs.get("list_non_text", False):
        validation_messages.append("List all non-text files.")
    if kwargs.get("list_queries", False):
        validation_messages.append("List all stored queries.")
    if not is_empty(kwargs.get("remove_query", None)):
        validation_messages.append("Remove the stored query.")

    if len(validation_messages) > 1:
        print(
            "You have requested multiple terminating options. Please specify only one."
        )
        print("Requested options:")
        for message in validation_messages:
            print(message)

        sys.exit()
