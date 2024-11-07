"""Command options decorators"""

from click import option, Command

from command_interface.help_text import (
    COMMAND_OPTION_COLUMN_NAMES_TEXT,
    COLUMN_OPTION_EXAMPLE,
    SORT_OPTION_EXAMPLE,
    AVAILABLE_SORT_TEXT,
    AVAILABLE_SIGNS_TEXT,
    AVAILABLE_TABLE_LIBS_TEXT,
)
from defaults.command import (
    DEFAULT_COLUMNS,
    DEFAULT_SORT,
)
from enums.application import TableLibrary


def columns_option(func) -> Command:
    """Columns option decorator"""
    return option(
        "--columns",
        default=DEFAULT_COLUMNS,
        help=f"""
            Column names: {COMMAND_OPTION_COLUMN_NAMES_TEXT}\n
            Example of input: --columns={COLUMN_OPTION_EXAMPLE}
        """,
    )(func)


def sort_option(func) -> Command:
    """Sort option decorator"""
    return option(
        "--sort",
        default=DEFAULT_SORT,
        help=f"""
            Column names: {COMMAND_OPTION_COLUMN_NAMES_TEXT}\n
            Sort variants: {AVAILABLE_SORT_TEXT}\n
            Example of input: --sort={SORT_OPTION_EXAMPLE}
        """,
    )(func)


def filter_option(func) -> Command:
    """Filters option decorator"""
    return option(
        "--filters",
        default=None,
        help=f"""
            Column names: {COMMAND_OPTION_COLUMN_NAMES_TEXT}\n
            Available signs: {AVAILABLE_SIGNS_TEXT}\n
            Example of input: --filters="linecount>50 and daratio>0.5"
        """,
    )(func)


def query_option(func) -> Command:
    """Query option decorator"""
    return option(
        "--query",
        default="",
        help=f"""
            Provide query\n
            Column names: {COMMAND_OPTION_COLUMN_NAMES_TEXT}\n
            Sort variants: {AVAILABLE_SORT_TEXT}\n
            Available signs: {AVAILABLE_SIGNS_TEXT}\n
            Example of input: SHOW linecount, daratio FROM ./ WHERE linecount > 100 and daratio < 1\n
            ORDER BY daratio ASC and linecount DESC\n
            Note! When query option provided, options: columns, filters, sort - are ignored
        """,
    )(func)


def non_text_files_option(func) -> Command:
    """Option to list all non text files in GIT repository"""
    return option(
        "--nontext",
        is_flag=True,
        help="""
            List all non-text files which are in GIT repository
            (includes only committed files)
            Note! When nontext option provided, all other options are ignored
        """,
    )(func)


def until_option(func) -> Command:
    """Until/before option"""
    return option(
        "--until",
        "--before",
        default=None,
        help="""
            Specify the date until which to gather git logs.
            Format: YYYY-MM-DD
        """,
    )(func)


def since_option(func) -> Command:
    """Since/after option"""
    return option(
        "--since",
        "--after",
        default=None,
        help="""
            Specify the date since which to gather git logs.
            Format: YYYY-MM-DD
        """,
    )(func)


def table_option(func) -> Command:
    """Table choice option"""
    return option(
        "--table",
        default=TableLibrary.PRETTY_TABLE.value,
        help=f"""
            Specify which CLI table you want to use: {AVAILABLE_TABLE_LIBS_TEXT}
        """,
    )(func)
