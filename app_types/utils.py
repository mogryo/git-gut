"""Types and enums for utils."""
from typing import TypedDict, Optional, List
from dataclasses import dataclass
from app_types.protocols import CliTable
from enums.columns import CliTableColumn


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
    added_lines: int
    removed_lines: int
    author: str


class ColumnBuilderKwargs(TypedDict):
    """Kwargs for ColumnBuilder"""
    pathname_length: Optional[int]
