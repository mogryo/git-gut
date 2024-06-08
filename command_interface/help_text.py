"""Help text generation"""

from command_interface.parameter_lists import (
    COMMAND_OPTION_COLUMN_NAMES,
    AVAILABLE_CELL_COLORS,
    AVAILABLE_SORT,
    AVAILABLE_SIGNS,
)
from enums.columns import CliTableColumn


COLUMN_OPTION_EXAMPLE = (
    f"{CliTableColumn.FILE_NAME.value},{CliTableColumn.LINE_COUNT.value}"
)
SORT_OPTION_EXAMPLE = (
    f"{CliTableColumn.FILE_NAME.value}-asc," f"{CliTableColumn.LINE_COUNT.value}-desc"
)
COMMAND_OPTION_COLUMN_NAMES_TEXT = ", ".join(COMMAND_OPTION_COLUMN_NAMES)
AVAILABLE_CELL_COLORS_TEXT = ", ".join(AVAILABLE_CELL_COLORS)
AVAILABLE_SORT_TEXT = ", ".join(AVAILABLE_SORT)
AVAILABLE_SIGNS_TEXT = ", ".join(AVAILABLE_SIGNS)
