"""Command option parsers"""
from typing import List, Optional, Dict

from app_types.dataclasses import SortingRule, NumberColumnColorCondition
from enums.columns import CliTableColumn, SortingDirection, CliTableColumnColor

REVERSE_COLUMN_NAME_MAPPING = {
    cli_table_column.value: cli_table_column for cli_table_column in CliTableColumn
}

REVERSE_SORTING_MAPPING = {
    sorting_direction.value: sorting_direction for sorting_direction in SortingDirection
}

COLOR_MAPPING = {
    color_enum_string.upper(): CliTableColumnColor[
        color_enum_string
    ] for color_enum_string in list(
        filter(lambda field: not field.startswith('_'), dir(CliTableColumnColor))
    )
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


def parse_option_color(
        color_string: Optional[str] = ""
) -> Dict[CliTableColumn, List[NumberColumnColorCondition]]:
    """
    Split single string into list of color conditions
    Format: column_name-0,0.15,green/0.15,0.3,yellow/0.3,,RED;...
    :param color_string: String with color conditions
    :return: Color condition list
    """
    result: Dict[CliTableColumn, List[NumberColumnColorCondition]] = {}

    for str_color_condition in color_string.split(';'):
        if str_color_condition.strip() == '':
            continue

        column_name = str_color_condition.split('-')[0]
        str_ranges = str_color_condition.split('-')[1].split('/')
        color_conditions: List[NumberColumnColorCondition] = []
        for str_range in str_ranges:
            split_range = str_range.split(',')
            color_conditions.append(
                NumberColumnColorCondition(
                    float(split_range[0]) if split_range[0] != '' else None,
                    float(split_range[1]) if split_range[1] != '' else None,
                    COLOR_MAPPING[split_range[2].upper()],
                )
            )
        result[REVERSE_COLUMN_NAME_MAPPING[column_name]] = color_conditions

    return result
