"""Command option parsers"""
from typing import List
from enums.columns import CliTableColumn


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


def parse_option_columns(columns_string: str) -> List[CliTableColumn]:
    """
    Split single string into list with separate column names.
    :param columns_string: String with technical names of table column.
    :return: Columns in list.
    """
    return list(
        map(
            lambda x: REVERSE_COLUMN_NAME_MAPPING[x],
            filter(lambda x: x != "", "".join(columns_string.split(" ")).split(","))
        )
    )
