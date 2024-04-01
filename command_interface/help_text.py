"""Help text generation"""
from enums.columns import CliTableColumn, CliTableColumnColor, SortingDirection

COMMAND_OPTION_COLUMN_NAMES = list(
    filter(lambda field: not field.startswith('_'), dir(CliTableColumn))
)
AVAILABLE_CELL_COLORS = list(
    map(
        lambda color: color.lower(),
        filter(lambda field: not field.startswith('_'), dir(CliTableColumnColor))
    )
)
AVAILABLE_SORT = list(
    map(
        lambda color: color.lower(),
        filter(lambda field: not field.startswith('_'), dir(SortingDirection))
    )
)
COLUMN_OPTION_EXAMPLE = f"{CliTableColumn.FILE_NAME.value},{CliTableColumn.LINE_COUNT.value}"
SORT_OPTION_EXAMPLE = f"{CliTableColumn.FILE_NAME.value}-asc," \
    f"{CliTableColumn.LINE_COUNT.value}-desc"
