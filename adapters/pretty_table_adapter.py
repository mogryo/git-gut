"""Adapter for pretty table to suit common interface (protocol)"""

from typing import List, Any
from prettytable import PrettyTable


class PrettyTableAdapter:
    """Adapter for CLI table"""

    def __init__(self):
        """Constructor"""
        self._table = PrettyTable()

    def add_row(self, row: List[Any]) -> None:
        """Add row to a table"""
        self._table.add_row(row)

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
