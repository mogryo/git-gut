"""Command option validators"""

import sys

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
