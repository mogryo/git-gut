"""Types and enums for utils."""
from typing import TypedDict, Optional, List
from enum import Enum
from dataclasses import dataclass
from app_types.protocols import CliTable


class CliTableColumn(Enum):
    """Enum for table column technical names"""
    ID = "id"
    FILE_NAME = "filename"
    COMMIT_AMOUNT = "commitcount"


class CliTableColumnLabel(Enum):
    """Enum for table column labels"""
    ID = "ID"
    FILENAME = "Filename"
    COMMITCOUNT = "Commit amount"


class GenerateUniqueKeysKwargs(TypedDict):
    """Kwargs for generating unique keys"""
    start_key: int
    end_key: int
    key_length: Optional[int]


class DrawFlatTreeTableKwargs(TypedDict):
    """Kwargs for building flat tree table"""
    path: str
    pathname_length: Optional[int]
    cli_table: Optional[CliTable]
    columns: Optional[List[CliTableColumn]]


@dataclass
class FileCommitStats:
    """Dataclass for file commit stats information"""
    added_lines: str
    removed_lines: str


class ColumnBuilderKwargs(TypedDict):
    """Kwargs for ColumnBuilder"""
    pathname_length: Optional[int]
