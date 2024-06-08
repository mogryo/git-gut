"""Lists of various command parameters"""

from enums.columns import CliTableColumn, CliTableColumnColor, SortingDirection
from query_option_parser.string_tokens import ALLOWED_SIGNS

COMMAND_OPTION_COLUMN_NAMES = list(
    map(
        lambda field: CliTableColumn[field].value,
        filter(lambda field: not field.startswith("_"), dir(CliTableColumn)),
    ),
)
AVAILABLE_CELL_COLORS = list(
    map(
        lambda color: color.lower(),
        filter(lambda field: not field.startswith("_"), dir(CliTableColumnColor)),
    )
)
AVAILABLE_SORT = list(
    map(
        lambda color: color.lower(),
        filter(lambda field: not field.startswith("_"), dir(SortingDirection)),
    )
)
AVAILABLE_SIGNS = list(ALLOWED_SIGNS)
