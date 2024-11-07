"""Utils mappings"""

from enums.table import CliTableColumn

REVERSE_COLUMN_NAME_MAPPING = {
    cli_table_column.value: cli_table_column for cli_table_column in CliTableColumn
}
