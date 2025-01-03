"""Parser generated nodes"""

import ast
from dataclasses import dataclass
from typing import List, Optional

from app_types.generics import Number
from enums.table import SortingDirection, CliTableColumn


@dataclass
class ConditionNode:
    """Condition statement"""

    column_name: str
    sign: str
    constant_part: Number | str


@dataclass
class SortRuleNode:
    """Order single rule statement"""

    column_name: CliTableColumn
    sort_direction: SortingDirection


@dataclass
class ShowNode:
    """Show statement"""

    column_names: List[CliTableColumn]


@dataclass
class WhereNode:
    """Where clause statement"""

    condition_node: Optional[ast.BoolOp]


@dataclass
class OrderNode:
    """Order statement"""

    sort_rule_nodes: List[SortRuleNode]


@dataclass
class FromNode:
    """From statement"""

    path: str


@dataclass
class SinceNode:
    """Since statement"""

    date: str


@dataclass
class IntervalNode:
    """Interval statement"""

    since: Optional[str]
    until: Optional[str]


@dataclass
class StatementNode:
    """Root of show statements"""

    show_node: Optional[ShowNode]
    where_node: Optional[WhereNode]
    order_node: Optional[OrderNode]
    from_node: Optional[FromNode]
    interval_node: Optional[IntervalNode]
