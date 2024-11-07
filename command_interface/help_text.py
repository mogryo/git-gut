"""Help text generation"""

from command_interface.parameter_lists import (
    COMMAND_OPTION_COLUMN_NAMES,
    AVAILABLE_SORT,
    AVAILABLE_SIGNS,
    AVAILABLE_TABLE_LIBS,
)
from enums.table import CliTableColumn


COLUMN_OPTION_EXAMPLE = (
    f"{CliTableColumn.FILE_NAME.value},{CliTableColumn.LINE_COUNT.value}"
)
SORT_OPTION_EXAMPLE = (
    f"{CliTableColumn.FILE_NAME.value} ASC" f"{CliTableColumn.LINE_COUNT.value} DESC"
)
COMMAND_OPTION_COLUMN_NAMES_TEXT = ", ".join(COMMAND_OPTION_COLUMN_NAMES)
AVAILABLE_SORT_TEXT = ", ".join(AVAILABLE_SORT)
AVAILABLE_SIGNS_TEXT = ", ".join(AVAILABLE_SIGNS)
AVAILABLE_TABLE_LIBS_TEXT = ", ".join(AVAILABLE_TABLE_LIBS)
