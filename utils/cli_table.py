"""Table functions"""
from typing import Optional, List, Any
from app_types.protocols import CliTable
from enums.columns import CliTableColumnLabel, CliTableColumn


def draw_flat_tree_table(
    column_technical_names: Optional[List[CliTableColumn]],
    rows: List[List[Any]],
    pretty_table: CliTable,
) -> None:
    """
    Draws basic table of flattened git tree, with specific columns.
    :param column_technical_names: Column names
    :param rows: Rows
    :param pretty_table: Instance of pretty table
    :return: None
    """
    pretty_table.field_names = list(
        map(lambda x: CliTableColumnLabel[x.value.upper()].value, column_technical_names)
    )
    for row in rows:
        pretty_table.add_row(row)

    print(pretty_table)
