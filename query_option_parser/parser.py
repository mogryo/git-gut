"""Parser functions"""
from string import punctuation, ascii_letters, digits
from typing import List, Optional, Tuple

from enums.columns import SortingDirection, CliTableColumn
from query_option_parser.nodes import ConditionNode, ShowNode, OrderNode, SortRuleNode,\
    StatementNode, FromNode, WhereNode
from query_option_parser.string_tokens import ALLOWED_SIGNS, TEXT_SIGNS,\
    TOP_LEVEL_STATEMENT_KEYWORDS
from command_interface.help_text import COMMAND_OPTION_COLUMN_NAMES
from utils.command_option_parser import REVERSE_COLUMN_NAME_MAPPING


def is_column_name(text: str) -> bool:
    """Check if word is column name"""
    return text in COMMAND_OPTION_COLUMN_NAMES


def is_sign(text: str) -> bool:
    """Check if word is sign in condition"""
    return text in ALLOWED_SIGNS


def is_text_sign(text: str) -> bool:
    """Check if text is a sign, which can be applied to a text"""
    return text in TEXT_SIGNS


def is_number(text: str) -> bool:
    """Check if text is a number"""
    try:
        float(text)
        return True
    except ValueError:
        return False


def is_allowed_condition(column_name: str, sign: str, constant_part: str) -> bool:
    """Check if condition is allowed"""
    return is_column_name(column_name) and is_sign(sign)\
        and (is_number(constant_part) or is_text_sign(constant_part))


def is_valid_sort(
        column_name: CliTableColumn | None,
        sort_direction: SortingDirection | None,
) -> bool:
    """Check if sort is valid"""
    return isinstance(column_name, CliTableColumn) and isinstance(sort_direction, SortingDirection)


def split_sign_condition_string(condition_string: str) -> Tuple[str, str, str]:
    """Split single condition intro three parts"""
    column_name: str = ""
    sign: str = ""
    constant_part: str = ""
    for char in condition_string:
        if char in ascii_letters and len(sign) == 0:
            column_name += char
        elif (char in ascii_letters or char in digits or char in {".", ","}) and len(sign) > 0:
            constant_part += char
        elif char in punctuation:
            sign += char

    return column_name, sign, constant_part


def split_sort_rule_string(
        sort_string: str,
) -> Tuple[CliTableColumn | None, SortingDirection | None]:
    """Split single sort rule into two parts"""
    split_sort = sort_string.split()
    sorting_enum_keys = list(filter(lambda x: not x.startswith('_'), dir(SortingDirection)))
    column_names = list(filter(lambda x: not x.startswith('_'), dir(CliTableColumn)))

    column_name = next(
        (
            name for name in column_names
            if len(split_sort) == 2 and CliTableColumn[name].value.upper() == split_sort[0].upper()
        ),
        None,
    )
    sorting_direction = next(
        (
            key for key in sorting_enum_keys
            if len(split_sort) == 2
            and SortingDirection[key].value.upper() == split_sort[1].upper()
        ),
        None,
    )

    return (
        CliTableColumn[column_name] if column_name is not None else None,
        SortingDirection[sorting_direction] if sorting_direction is not None else None
    )


def parse_where_statement(where_statement: Optional[str] = "") -> WhereNode:
    """Parse where statement"""
    condition_nodes: List[ConditionNode] = []
    for condition in where_statement.split(' and '):
        column_name, sign, constant = split_sign_condition_string(condition)
        if is_allowed_condition(column_name, sign, constant):
            condition_nodes.append(
                ConditionNode(
                    column_name=column_name,
                    sign=sign,
                    constant_part=float(constant) if is_number(constant) else constant
                )
            )

    return WhereNode(condition_nodes)


def parse_show_statement(show_statement: Optional[str] = "") -> ShowNode:
    """Parse show statement"""
    string_column_names = show_statement.replace(' ', '').split(',')

    enum_column_names: List[CliTableColumn] = []
    for column_name in string_column_names:
        if is_column_name(column_name):
            enum_column_names.append(REVERSE_COLUMN_NAME_MAPPING[column_name])

    return ShowNode(enum_column_names)


def parse_order_statement(order_statement: Optional[str] = "") -> OrderNode:
    """Parse order(sort) statement"""
    sort_rule_nodes: List[SortRuleNode] = []
    for sort_rule in order_statement.split(' and '):
        column_name, sort_direction = split_sort_rule_string(sort_rule)
        if is_valid_sort(column_name, sort_direction):
            sort_rule_nodes.append(SortRuleNode(column_name, sort_direction))

    return OrderNode(sort_rule_nodes)


def parse_from_statement(from_statement: Optional[str] = "") -> FromNode:
    """Parse from statement"""
    return FromNode(from_statement)


TOP_LEVEL_STATEMENT_PARSERS = {
    'SHOW': parse_show_statement,
    'FROM': parse_from_statement,
    'WHERE': parse_where_statement,
    'ORDERBY': parse_order_statement,
}

ROOT_NODE_KEYS = {
    'SHOW': "show_node",
    'FROM': "from_node",
    'WHERE': "where_node",
    'ORDERBY': "order_node",
}


def parse_root_statement(statement: Optional[str] = "") -> StatementNode:
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


if __name__ == "__main__":
    parse_root_statement("SHOW linecount, daratio")
