from typing import TypedDict, Optional, List
from app_types.protocols import CliTable
from dataclasses import dataclass
from enum import Enum


class CliTableColumn(Enum):
    ID = "id"
    FILE_NAME = "filename"
    COMMIT_AMOUNT = "commitcount"


class CliTableColumnLabel(Enum):
    id = "ID"
    filename = "Filename"
    commitcount = "Commit amount"


class GenerateUniqueKeysKwargs(TypedDict):
    start_key: int
    end_key: int
    key_length: Optional[int]


class DrawFlatTreeTableKwargs(TypedDict):
    path: str
    pathname_length: Optional[int]
    cli_table: Optional[CliTable]
    columns: Optional[List[CliTableColumn]]


@dataclass
class FileCommitStats:
    added_lines: str
    removed_lines: str


class ColumnBuilderKwargs(TypedDict):
    pathname_length: Optional[int]
