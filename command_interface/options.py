"""Command options decorators"""
from click import option, Command

from command_interface.help_text import COMMAND_OPTION_COLUMN_NAMES_TEXT, COLUMN_OPTION_EXAMPLE, \
    SORT_OPTION_EXAMPLE, AVAILABLE_CELL_COLORS_TEXT, AVAILABLE_SORT_TEXT, AVAILABLE_SIGNS_TEXT
from defaults.command import DEFAULT_COLUMNS, DEFAULT_SORT, DEFAULT_COLORS, DEFAULT_FILTERS


def columns_option(func) -> Command:
    """Columns option decorator"""
    return option(
        "--columns",
        default=DEFAULT_COLUMNS,
        help=f"""
            Column names: ${COMMAND_OPTION_COLUMN_NAMES_TEXT}
            Example of input: --columns={COLUMN_OPTION_EXAMPLE}
        """
    )(func)


def sort_option(func) -> Command:
    """Sort option decorator"""
    return option(
        "--sort",
        default=DEFAULT_SORT,
        help=f"""
            Column names: ${COMMAND_OPTION_COLUMN_NAMES_TEXT}
            Sort variants: ${AVAILABLE_SORT_TEXT}
            Example of input: --sort={SORT_OPTION_EXAMPLE}
        """
    )(func)


def colors_option(func) -> Command:
    """Colors option decorator"""
    return option(
        "--colors",
        default=DEFAULT_COLORS,
        help=f"""
            Column names: ${COMMAND_OPTION_COLUMN_NAMES_TEXT}
            Available colors: ${AVAILABLE_CELL_COLORS_TEXT}
            Example of input: --colors=daratio-0,0.15,green/0.15,0.3,yellow/0.3,,red;
        """
    )(func)


def filter_option(func) -> Command:
    """Filters option decorator"""
    return option(
        "--filters",
        default=DEFAULT_FILTERS,
        help=f"""
            Column names: ${COMMAND_OPTION_COLUMN_NAMES_TEXT}
            Available sings: ${AVAILABLE_SIGNS_TEXT}
            Example of input: --filters="linecount>50 and daratio>0.5"
        """
    )(func)


def query_option(func) -> Command:
    """Query option decorator"""
    return option(
        "--query",
        default="",
        help=f"""
            Provide query
            Column names: ${COMMAND_OPTION_COLUMN_NAMES_TEXT}
            Sort variants: ${AVAILABLE_SORT_TEXT}
            Available sings: ${AVAILABLE_SIGNS_TEXT}
            Example of input: SHOW linecount, daratio FROM ./ WHERE linecount > 100 and daratio < 1
            ORDER BY daratio ASC and linecount DESC
            Note! When query option provided, options: columns, filters, sort - are ignored
        """
    )(func)
