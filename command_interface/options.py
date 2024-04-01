"""Command options decorators"""
from click import option, Command

from command_interface.help_text import COMMAND_OPTION_COLUMN_NAMES, COLUMN_OPTION_EXAMPLE, \
    AVAILABLE_SORT, SORT_OPTION_EXAMPLE, AVAILABLE_CELL_COLORS
from defaults.command import DEFAULT_COLUMNS, DEFAULT_SORT, DEFAULT_COLORS


def columns_option(func) -> Command:
    """Columns option decorator"""
    return option(
        "--columns",
        default=DEFAULT_COLUMNS,
        help=f"""
            Column names: ${COMMAND_OPTION_COLUMN_NAMES}
            Example of input: --columns={COLUMN_OPTION_EXAMPLE}
        """
    )(func)


def sort_option(func) -> Command:
    """Sort option decorator"""
    return option(
        "--sort",
        default=DEFAULT_SORT,
        help=f"""
            Column names: ${COMMAND_OPTION_COLUMN_NAMES}
            Sort variants: ${AVAILABLE_SORT}
            Example of input: --sort={SORT_OPTION_EXAMPLE}
        """
    )(func)


def colors_option(func) -> Command:
    """Colors option decorator"""
    return option(
        "--colors",
        default=DEFAULT_COLORS,
        help=f"""
            Column names: ${COMMAND_OPTION_COLUMN_NAMES}
            Available colors: ${AVAILABLE_CELL_COLORS}
            Example of input: --colors=daratio-0,0.15,green/0.15,0.3,yellow/0.3,,red;
        """
    )(func)
