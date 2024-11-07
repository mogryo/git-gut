"""Lists of various command parameters"""

from enums.table import CliTableColumn, SortingDirection

from enums.application import TableLibrary
from query_option_parser.string_tokens import ALLOWED_SIGNS

COMMAND_OPTION_COLUMN_NAMES = list(
    map(
        lambda field: CliTableColumn[field].value,
        filter(lambda field: not field.startswith("_"), dir(CliTableColumn)),
    ),
)
AVAILABLE_SORT = list(
    map(
        lambda sort: sort.lower(),
        filter(lambda field: not field.startswith("_"), dir(SortingDirection)),
    )
)
AVAILABLE_SIGNS = list(ALLOWED_SIGNS)
AVAILABLE_TABLE_LIBS = [
    TableLibrary[lib].value for lib in dir(TableLibrary) if not lib.startswith("_")
]
