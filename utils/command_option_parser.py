"""Command option parsers"""

from typing import List, Optional, Dict

from app_types.dataclasses import SeparateOptionsAsQuery, NumberColumnColorCondition
from enums.columns import CliTableColumn
from query_option_parser.nodes import StatementNode
from query_option_parser.parser import TOP_LEVEL_STATEMENT_PARSERS, ROOT_NODE_KEYS
from query_option_parser.string_tokens import TOP_LEVEL_STATEMENT_KEYWORDS
from utils.mappings import (
    REVERSE_COLUMN_NAME_MAPPING,
    COLOR_MAPPING,
)


def parse_option_color(
    color_string: Optional[str],
) -> Dict[CliTableColumn, List[NumberColumnColorCondition]]:
    """
    Split single string into list of color conditions
    Format: column_name-0,0.15,green/0.15,0.3,yellow/0.3,,RED;...
    :param color_string: String with color conditions
    :return: Color condition list
    """
    result: Dict[CliTableColumn, List[NumberColumnColorCondition]] = {}

    for str_color_condition in (color_string or "").split(";"):
        if str_color_condition.strip() == "":
            continue

        column_name = str_color_condition.split("-")[0]
        str_ranges = str_color_condition.split("-")[1].split("/")
        color_conditions: List[NumberColumnColorCondition] = []
        for str_range in str_ranges:
            split_range = str_range.split(",")
            color_conditions.append(
                NumberColumnColorCondition(
                    float(split_range[0]) if split_range[0] != "" else 0,
                    float(split_range[1]) if split_range[1] != "" else None,
                    COLOR_MAPPING[split_range[2].upper()],
                )
            )
        result[REVERSE_COLUMN_NAME_MAPPING[column_name]] = color_conditions

    return result


def parse_option_query(statement: Optional[str]) -> StatementNode:
    """Parse whole statement"""
    active_statement: str | None = None
    accumulated_text: List[str] = []
    root_node = StatementNode(None, None, None, None, None)

    split_text = statement.split() if statement is not None else []
    for index, word in enumerate(split_text):
        if word.upper() not in TOP_LEVEL_STATEMENT_KEYWORDS:
            accumulated_text.append(word)
        if word.upper() in TOP_LEVEL_STATEMENT_KEYWORDS or (index + 1) == len(split_text):
            if active_statement in TOP_LEVEL_STATEMENT_PARSERS:
                node = TOP_LEVEL_STATEMENT_PARSERS[active_statement](
                    " ".join(accumulated_text)
                )
                setattr(root_node, ROOT_NODE_KEYS[active_statement], node)
                accumulated_text.clear()
            active_statement = word

    return root_node


def parse_separate_options_into_query(options: SeparateOptionsAsQuery) -> str:
    statement_parts: List[str] = []
    if options.columns is not None:
        statement_parts.append(f"SHOW {options.columns}")

    statement_parts.append(f"FROM {options.file_path}")

    if options.filters is not None:
        statement_parts.append(f"WHERE {options.filters}")

    if options.sort is not None:
        statement_parts.append(f"ORDERBY {options.sort}")

    if options.since is not None:
        statement_parts.append(f"SINCE {options.since}")

    if options.until is not None:
        statement_parts.append(f"UNTIL {options.until}")

    return " ".join(statement_parts)
