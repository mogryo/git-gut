"""Parser functions"""

import ast
import sys
from typing import List, Optional, Tuple, cast

from enums.columns import SortingDirection, CliTableColumn
from query_option_parser.nodes import (
    IntervalNode,
    ShowNode,
    OrderNode,
    SortRuleNode,
    FromNode,
    WhereNode,
)
from command_interface.help_text import COMMAND_OPTION_COLUMN_NAMES
from utils.mappings import REVERSE_COLUMN_NAME_MAPPING


def is_column_name(text: str) -> bool:
    """Check if word is column name"""
    return text in COMMAND_OPTION_COLUMN_NAMES


def is_valid_sort(
    column_name: CliTableColumn | None,
    sort_direction: SortingDirection | None,
) -> bool:
    """Check if sort is valid"""
    return isinstance(column_name, CliTableColumn) and isinstance(
        sort_direction, SortingDirection
    )


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


def parse_where_statement(where_statement: Optional[str] = "") -> WhereNode:
    """Parse statement with Python ast module"""
    if where_statement is None or where_statement.strip() == "":
        return WhereNode(None)

    corrected_where_statement = where_statement.replace(" AND ", " and ").replace(" OR ", " or ").replace(" NOT ", " not ")
    parsed_statement = ast.parse(f"""if {corrected_where_statement }: \n\tpass""")
    return WhereNode(cast(ast.BoolOp, cast(ast.If, parsed_statement.body[0]).test))


def parse_show_statement(show_statement: Optional[str]) -> ShowNode:
    """Parse show statement"""
    string_column_names = (show_statement or "").replace(" ", "").split(",")

    enum_column_names: List[CliTableColumn] = []
    for column_name in string_column_names:
        if is_column_name(column_name):
            enum_column_names.append(REVERSE_COLUMN_NAME_MAPPING[column_name])

    return ShowNode(enum_column_names)


def parse_order_statement(order_statement: Optional[str]) -> OrderNode:
    """Parse order(sort) statement"""
    sort_rule_nodes: List[SortRuleNode] = []
    for sort_rule in (order_statement or "").replace(" AND ", " and ").split(" and "):
        column_name, sort_direction = split_sort_rule_string(sort_rule)
        if is_valid_sort(column_name, sort_direction):
            sort_rule_nodes.append(SortRuleNode(column_name, sort_direction))

    return OrderNode(sort_rule_nodes)


def parse_from_statement(from_statement: Optional[str] = "") -> FromNode:
    """Parse from statement"""
    return FromNode(from_statement if from_statement is not None else "")


def parse_interval_statement(interval_statement: Optional[str] = "") -> IntervalNode:
    """Parse interval statement"""
    split_words = (
        [word.upper() for word in interval_statement.split()]
        if interval_statement is not None
        else []
    )

    if not (len(split_words) == 2 or len(split_words) == 4):
        print("Please specify correct INTERVAL")
        sys.exit()

    since: str | None = None
    until: str | None = None
    if len(split_words) > 1:
        if split_words[0] == "SINCE" or split_words[0] == "AFTER":
            since = split_words[1]
        elif split_words[0] == "UNTIL" or split_words[0] == "BEFORE":
            until = split_words[1]

    if len(split_words) == 4:
        if split_words[2] == "SINCE" or split_words[2] == "AFTER":
            since = split_words[3]
        elif split_words[2] == "UNTIL" or split_words[2] == "BEFORE":
            until = split_words[3]

    return IntervalNode(since, until)


TOP_LEVEL_STATEMENT_PARSERS = {
    "SHOW": parse_show_statement,
    "FROM": parse_from_statement,
    "WHERE": parse_where_statement,
    "ORDERBY": parse_order_statement,
    "INTERVAL": parse_interval_statement,
}

ROOT_NODE_KEYS = {
    "SHOW": "show_node",
    "FROM": "from_node",
    "WHERE": "where_node",
    "ORDERBY": "order_node",
    "INTERVAL": "interval_node",
}
