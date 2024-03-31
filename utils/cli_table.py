"""Table functions"""
from typing import Optional, List, Any
from app_types.protocols import CliTable
from enums.columns import CliTableColumnLabel, CliTableColumn
from utils.id_generator import generate_unique_keys


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
    pretty_table.field_names = [CliTableColumnLabel.ID.value.upper()] + list(
        map(lambda x: CliTableColumnLabel[x.value.upper()].value, column_technical_names)
    )
    unique_keys = generate_unique_keys(
        start_key=1, end_key=len(rows), key_length=len(str(len(rows)))
    )
    for unique_key, row in zip(unique_keys, rows):
        pretty_table.add_row([unique_key, *row])

    print(pretty_table)
