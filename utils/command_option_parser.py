"""Command option parsers"""
from typing import List, AnyStr


def parse_option_columns(columns_string: str) -> List[AnyStr]:
    """
    Split single string into list with separate column names.
    :param columns_string: String with technical names of table column.
    :return: Columns in list.
    """
    return list(filter(lambda x: x != "", "".join(columns_string.split(" ")).split(",")))
