"""Enums for column data"""
from enum import Enum


class CliTableColumn(Enum):
    """Enum for table column technical names"""
    ID = "id"
    FILE_NAME = "filename"
    COMMIT_AMOUNT = "commitcount"
    MOST_FREQUENT_AUTHOR = "mfauthor"
    MOST_ADDED_AUTHOR = "maauthor"
    MOST_DELETED_AUTHOR = "mdauthor"
    DELETED_ADDED_RATIO = "daratio"
    LINE_COUNT = "linecount"


class CliTableColumnLabel(Enum):
    """Enum for table column labels"""
    ID = "ID"
    FILENAME = "Filename"
    COMMITCOUNT = "Commit amount"
    MFAUTHOR = "Most frequent author"
    MAAUTHOR = "Most + lines by (amount)"
    MDAUTHOR = "Most - lines by (amount)"
    DARATIO = "Delete/Add ratio"
    LINECOUNT = "Line count"


class CliTableColumnColor(Enum):
    """Enum for table column colors"""
    RED = "\033[0;31;40m"
    GREEN = "\033[0;32;40m"
    YELLOW = "\033[0;33;40m"
    BLUE = "\033[0;34;40m"
    RESET = "\033[0m"


class SortingDirection(Enum):
    """Enum for sorting direction"""
    ASC = 'ascending'
    DESC = 'descending'
