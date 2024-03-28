"""Command option parsers"""
from typing import List, Optional

from app_types.dataclasses import SortingRule
from enums.columns import CliTableColumn, SortingDirection

REVERSE_COLUMN_NAME_MAPPING = {
    CliTableColumn.ID.value: CliTableColumn.ID,
    CliTableColumn.FILE_NAME.value: CliTableColumn.FILE_NAME,
    CliTableColumn.COMMIT_AMOUNT.value: CliTableColumn.COMMIT_AMOUNT,
    CliTableColumn.MOST_FREQUENT_AUTHOR.value: CliTableColumn.MOST_FREQUENT_AUTHOR,
    CliTableColumn.MOST_ADDED_AUTHOR.value: CliTableColumn.MOST_ADDED_AUTHOR,
    CliTableColumn.MOST_DELETED_AUTHOR.value: CliTableColumn.MOST_DELETED_AUTHOR,
    CliTableColumn.DELETED_ADDED_RATIO.value: CliTableColumn.DELETED_ADDED_RATIO,
    CliTableColumn.LINE_COUNT.value: CliTableColumn.LINE_COUNT,
}

REVERSE_SORTING_MAPPING = {
    SortingDirection.ASC.value: SortingDirection.ASC,
    SortingDirection.DESC.value: SortingDirection.DESC,
}


def parse_option_columns(columns_string: str) -> List[CliTableColumn]:
    """
    Split single string into list with separate column names
    :param columns_string: String with technical names of table column
    :return: Columns in list
    """
    return list(
        map(
            lambda x: REVERSE_COLUMN_NAME_MAPPING[x],
            filter(lambda x: x != "", "".join(columns_string.split(" ")).split(","))
        )
    )


def parse_option_sort(sort_string: Optional[str] = "") -> List[SortingRule]:
    """
    Split single string into list of sorting rules
    :param sort_string: String with sorting rules in format column_name-asc/decs
    :return: Sorting rules in list
    """
    separate_string_rules = list(
        filter(lambda x: x != "", "".join(sort_string.split(" ")).split(","))
    )
    rules: List[SortingRule] = []
    for rule_string in separate_string_rules:
        split_rule = rule_string.split("-")
        rules.append(
            SortingRule(
                REVERSE_COLUMN_NAME_MAPPING[split_rule[0]],
                REVERSE_SORTING_MAPPING[split_rule[1]],
            )
        )

    return rules
