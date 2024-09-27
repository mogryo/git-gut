"""Application dataclasses"""

from dataclasses import dataclass
from typing import Optional
from app_types.generics import Number
from enums.columns import CliTableColumnColor, SortingDirection, CliTableColumn


@dataclass
class FileCommitStats:
    """Dataclass for file commit stats information"""

    added_lines: int
    removed_lines: int
    author: str


@dataclass
class NumberColumnColorCondition:
    """Dataclass for column color condition, for numbers"""

    start: float
    end: Optional[float]
    color: CliTableColumnColor


@dataclass
class SortingRule:
    """Dataclass for sorting rules"""

    column_name: CliTableColumn
    sort_direction: SortingDirection


@dataclass
class GitLogOptions:
    """Dataclass for storing git log options"""

    since: Optional[str]
    until: Optional[str]


@dataclass
class SeparateOptionsAsQuery:
    """Dataclass for storing separate input options which form proper query"""

    columns: Optional[str]
    file_path: str
    sort: Optional[str]
    filters: Optional[str]
    since: Optional[str]
    until: Optional[str]
