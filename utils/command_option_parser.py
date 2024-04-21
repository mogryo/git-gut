"""Command option parsers"""
from typing import List, Optional, Dict

from app_types.dataclasses import SortingRule, NumberColumnColorCondition
from enums.columns import CliTableColumn
from query_option_parser.nodes import StatementNode
from query_option_parser.parser import TOP_LEVEL_STATEMENT_PARSERS, ROOT_NODE_KEYS
from query_option_parser.string_tokens import TOP_LEVEL_STATEMENT_KEYWORDS
from utils.mappings import REVERSE_COLUMN_NAME_MAPPING, REVERSE_SORTING_MAPPING, COLOR_MAPPING


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


def parse_option_query(statement: Optional[str] = "") -> StatementNode:
    """Parse whole statement"""
    active_statement: str | None = None
    accumulated_text: List[str] = []
    root_node = StatementNode(None, None, None, None)

    split_text = statement.split()
    for index, word in enumerate(split_text):
        if word not in TOP_LEVEL_STATEMENT_KEYWORDS:
            accumulated_text.append(word)
        if word in TOP_LEVEL_STATEMENT_KEYWORDS or (index + 1) == len(split_text):
            if active_statement in TOP_LEVEL_STATEMENT_PARSERS:
                node = TOP_LEVEL_STATEMENT_PARSERS[active_statement](' '.join(accumulated_text))
                setattr(root_node, ROOT_NODE_KEYS[active_statement], node)
                accumulated_text.clear()
            active_statement = word

    return root_node
