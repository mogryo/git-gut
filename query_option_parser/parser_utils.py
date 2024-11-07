"""Helper functions for parsers"""

from typing import Tuple, List

from app_types.result import ResultUnion, ResultValidationError, ResultOk
from app_types.validation_errors import NodeValidationError
from enums.application import Severity
from enums.table import CliTableColumn, SortingDirection


def split_sort_rule_string(
    sort_string: str,
) -> Tuple[CliTableColumn | None, SortingDirection | None]:
    """Split single sort rule into two parts"""
    split_sort = sort_string.split()
    sorting_enum_keys = list(
        filter(lambda x: not x.startswith("_"), dir(SortingDirection))
    )
    column_names = list(filter(lambda x: not x.startswith("_"), dir(CliTableColumn)))

    column_name = next(
        (
            name
            for name in column_names
            if len(split_sort) == 2
            and CliTableColumn[name].value.upper() == split_sort[0].upper()
        ),
        None,
    )
    sorting_direction = next(
        (
            key
            for key in sorting_enum_keys
            if len(split_sort) == 2
            and SortingDirection[key].value.upper() == split_sort[1].upper()
        ),
        None,
    )

    return (
        CliTableColumn[column_name] if column_name is not None else None,
        SortingDirection[sorting_direction] if sorting_direction is not None else None,
    )


def extract_since_and_until_interval(
    split_words: List[str] | Tuple[str, ...],
) -> ResultUnion[Tuple[str | None, str | None], NodeValidationError]:
    """Extract since/until intervals"""
    since: str | None = None
    until: str | None = None

    if split_words[0] == "SINCE" or split_words[0] == "AFTER":
        since = split_words[1]
    elif split_words[0] == "UNTIL" or split_words[0] == "BEFORE":
        until = split_words[1]
    else:
        return ResultValidationError(
            " ".join(split_words),
            [
                NodeValidationError(
                    " ".join(split_words),
                    "Invalid interval keyword - use one of SINCE/UNTIL/AFTER/BEFORE",
                    Severity.CRITICAL,
                )
            ],
        )

    return ResultOk((since, until))
