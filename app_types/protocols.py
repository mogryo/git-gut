from typing import Protocol, List, Any


class CliTable(Protocol):
    def __init__(self):
        self.field_names: List[str] = []

    def add_row(self, row: List[Any], *, divider: bool = False):
        pass
