"""Utils mappings"""
from enums.columns import CliTableColumn, SortingDirection, CliTableColumnColor

REVERSE_COLUMN_NAME_MAPPING = {
    cli_table_column.value: cli_table_column for cli_table_column in CliTableColumn
}

REVERSE_SORTING_MAPPING = {
    sorting_direction.value: sorting_direction for sorting_direction in SortingDirection
}

COLOR_MAPPING = {
    color_enum_string.upper(): CliTableColumnColor[
        color_enum_string
    ] for color_enum_string in list(
        filter(lambda field: not field.startswith('_'), dir(CliTableColumnColor))
    )
}
