"""Types for builders/pipelines"""
from dataclasses import dataclass
from typing import Optional
from app_types.generics import Number
from enums.columns import CliTableColumnColor, SortingDirection


@dataclass
class NumberColumnColorCondition:
    """Dataclass for column color condition, for numbers"""
    start: Number
    end: Optional[Number]
    color: CliTableColumnColor


@dataclass
class SortingRule:
    """Dataclass for sorting rules"""
    column_name: str
    sort_direction: SortingDirection
