"""Protocol classes for application"""

from typing import Protocol, List, Any


class CliTable(Protocol):
    """Protocol class for common table interface."""

    def __init__(self):
        """Constructor"""

    def add_row(self, row: Any, *, divider: bool = False):
        """Add row to table."""

    @property
    def field_names(self) -> List[str]:
        """Property for field_names"""

    @field_names.setter
    def field_names(self, val: Any):
        """Property setter for field_names"""

    def print(self) -> None:
        """Print table"""
