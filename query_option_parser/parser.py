"""Parser functions"""

import ast
from typing import List, Optional, Tuple, cast

from enums.columns import SortingDirection, CliTableColumn
from query_option_parser.nodes import (
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
    if where_statement.strip() == "":
        return WhereNode(None)

    parsed_statement = ast.parse(f"""if {where_statement}: \n\tpass""")
    return WhereNode(cast(ast.BoolOp, cast(ast.If, parsed_statement.body[0]).test))


def parse_show_statement(show_statement: Optional[str] = "") -> ShowNode:
    """Parse show statement"""
    string_column_names = show_statement.replace(" ", "").split(",")

    enum_column_names: List[CliTableColumn] = []
    for column_name in string_column_names:
        if is_column_name(column_name):
            enum_column_names.append(REVERSE_COLUMN_NAME_MAPPING[column_name])

    return ShowNode(enum_column_names)


def parse_order_statement(order_statement: Optional[str] = "") -> OrderNode:
    """Parse order(sort) statement"""
    sort_rule_nodes: List[SortRuleNode] = []
    for sort_rule in order_statement.split(" and "):
        column_name, sort_direction = split_sort_rule_string(sort_rule)
        if is_valid_sort(column_name, sort_direction):
            sort_rule_nodes.append(SortRuleNode(column_name, sort_direction))

    return OrderNode(sort_rule_nodes)


def parse_from_statement(from_statement: Optional[str] = "") -> FromNode:
    """Parse from statement"""
    return FromNode(from_statement)


TOP_LEVEL_STATEMENT_PARSERS = {
    "SHOW": parse_show_statement,
    "FROM": parse_from_statement,
    "WHERE": parse_where_statement,
    "ORDERBY": parse_order_statement,
}

ROOT_NODE_KEYS = {
    "SHOW": "show_node",
    "FROM": "from_node",
    "WHERE": "where_node",
    "ORDERBY": "order_node",
}
