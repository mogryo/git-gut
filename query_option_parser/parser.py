"""Parser functions"""
from string import punctuation, ascii_letters, digits
from typing import List, Optional, Tuple
from query_option_parser.nodes import ConditionNode
from query_option_parser.string_tokens import ALLOWED_SIGNS, TEXT_SIGNS
from command_interface.help_text import COMMAND_OPTION_COLUMN_NAMES


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


def parse_where_statement(where_statement: Optional[str] = "") -> List[ConditionNode]:
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

    return condition_nodes
