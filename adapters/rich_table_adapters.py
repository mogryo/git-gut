"""Adapter for rich table to suit common interface (protocol)"""

from typing import List, Any, Optional
from rich.table import Table
from rich.console import Console

from enums.table import AvailableTableRowColors

MAP_COLOR_TO_RICH_COLOR = {
    AvailableTableRowColors.GREEN: "green",
    AvailableTableRowColors.YELLOW: "yellow",
    AvailableTableRowColors.RED: "red",
}


class RichTableAdapter:
    """Adapter for CLI table"""

    def __init__(self):
        """Constructor"""
        self._table = Table()

    def add_row(self, row: List[Any], color: Optional[AvailableTableRowColors]) -> None:
        """Add row to a table"""
        if color is None:
            self._table.add_row(*row)
        else:
            self._table.add_row(*row, style=MAP_COLOR_TO_RICH_COLOR[color])

    @property
    def field_names(self) -> List[str]:
        """Property for field_names"""
        return [column.header for column in self._table.columns]

    @field_names.setter
    def field_names(self, column_names: List[str]):
        """Property setter for field_names"""
        for column_name in column_names:
            self._table.add_column(column_name, no_wrap=True)

    def print(self) -> None:
        """Print table"""
        console = Console()
        console.print(self._table)
