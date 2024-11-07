"""Application dataclasses"""

from dataclasses import dataclass
from typing import Optional
from enums.table import SortingDirection, CliTableColumn


@dataclass
class FileCommitStats:
    """Dataclass for file commit stats information"""

    added_lines: int
    removed_lines: int
    author: str


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

    columns: Optional[str] = None
    file_path: Optional[str] = None
    sort: Optional[str] = None
    filters: Optional[str] = None
    since: Optional[str] = None
    until: Optional[str] = None
