"""Adapter for pretty table to suit common interface (protocol)"""

from typing import List, Any, Optional
from prettytable import PrettyTable

from enums.table import AvailableTableRowColors, PrettyTableColumnColor

MAP_COLOR_TO_PRETTY_COLOR = {
    AvailableTableRowColors.GREEN: PrettyTableColumnColor.GREEN.value,
    AvailableTableRowColors.YELLOW: PrettyTableColumnColor.YELLOW.value,
    AvailableTableRowColors.RED: PrettyTableColumnColor.RED.value,
}


class PrettyTableAdapter:
    """Adapter for CLI table"""

    def __init__(self):
        """Constructor"""
        self._table = PrettyTable()

    def add_row(self, row: List[Any], color: Optional[AvailableTableRowColors]) -> None:
        """Add row to a table"""
        if color is None:
            self._table.add_row(*row)
        else:
            self._table.add_row(
                [
                    f"{MAP_COLOR_TO_PRETTY_COLOR[color]}{col}{PrettyTableColumnColor.RESET.value}"
                    for col in row
                ]
            )

    @property
    def field_names(self) -> List[str]:
        """Property for field_names"""
        return self._table.field_names

    @field_names.setter
    def field_names(self, column_names: List[str]) -> None:
        """Property setter for field_names"""
        self._table.field_names = column_names

    def print(self) -> None:
        """Print table"""
        print(self._table)
