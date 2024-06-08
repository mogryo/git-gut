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

    start: Number
    end: Optional[Number]
    color: CliTableColumnColor


@dataclass
class SortingRule:
    """Dataclass for sorting rules"""

    column_name: CliTableColumn
    sort_direction: SortingDirection
