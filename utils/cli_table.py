"""Table functions"""

from typing import Optional, List, Any, Tuple

from adapters.pretty_table_adapter import PrettyTableAdapter
from adapters.rich_table_adapters import RichTableAdapter
from app_types.protocols import CliTable
from app_types.result import ResultOk, ResultUnion, ResultValidationError
from app_types.validation_errors import InvalidTableLibraryError
from command_interface.help_text import AVAILABLE_TABLE_LIBS_TEXT
from defaults.command import DEFAULT_COLORS
from enums.application import TableLibrary, Severity
from enums.table import CliTableColumnLabel, CliTableColumn, AvailableTableRowColors
from utils.colors import ColorRanges, prioritize_color, get_color
from utils.id_generator import generate_unique_keys


def draw_flat_tree_table(
    column_technical_names: Optional[List[CliTableColumn]],
    rows: List[List[Any]],
    table: CliTable,
) -> None:
    """
    Draws basic table of flattened git tree, with specific columns.
    :param column_technical_names: Column names
    :param rows: Rows
    :param table: Instance of table
    :return: None
    """
    table.field_names = [CliTableColumnLabel.ID.value.upper()] + list(
        map(
            lambda x: CliTableColumnLabel[x.value.upper()].value, column_technical_names
        )
    )
    unique_keys = generate_unique_keys(
        start_key=1, end_key=len(rows), key_length=len(str(len(rows)))
    )

    colors_with_indexes: List[Tuple[CliTableColumn, ColorRanges, int]] = [
        (column_name, color, column_technical_names.index(column_name))
        for column_name, color in DEFAULT_COLORS
        if column_technical_names.index(column_name) > 0
    ]

    for unique_key, row in zip(unique_keys, rows):
        determined_color: AvailableTableRowColors | None = None
        for column_name, color_identifier, index in colors_with_indexes:
            determined_color = prioritize_color(
                get_color(row[index], color_identifier), determined_color
            )

        table.add_row(
            [unique_key, *[str(item) for item in row]],
            determined_color,
        )

    table.print()


def create_table_instance(
    table_option: str,
) -> ResultUnion[CliTable, InvalidTableLibraryError]:
    """Create requested library instance"""
    match table_option:
        case TableLibrary.PRETTY_TABLE.value:
            return ResultOk(PrettyTableAdapter())
        case TableLibrary.RICH_TABLE.value:
            return ResultOk(RichTableAdapter())

    return ResultValidationError(
        table_option,
        [
            InvalidTableLibraryError(
                table_option,
                f"Please specify correct table library, one of: {AVAILABLE_TABLE_LIBS_TEXT}",
                Severity.CRITICAL,
            )
        ],
    )
