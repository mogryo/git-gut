"""Parser generated nodes"""
from dataclasses import dataclass

from app_types.generics import Number


@dataclass
class ConditionNode:
    """Condition statement"""
    column_name: str
    sign: str
    constant_part: Number | str
