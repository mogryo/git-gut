"""Protocol classes for application"""

from typing import Protocol, List, Any


class CliTable(Protocol):
    """Protocol class for common table interface."""

    def __init__(self):
        self._field_names: List[str] = []

    def add_row(self, row: List[Any], *, divider: bool = False):
        """Add row to table."""

    @property
    def field_names(self):
        """Property for field_names"""
        return self._field_names

    @field_names.setter
    def field_names(self, new_field_names: List[str]):
        """Property setter for field_names"""
        self._field_names = new_field_names
