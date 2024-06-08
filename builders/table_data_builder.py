"""Builder for table"""

from collections import OrderedDict
from typing import Self, List, Any
from builders.column_data_builder import ColumnDataBuilder
from enums.columns import CliTableColumn


class TableDataBuilder:
    """Builder for table data"""

    def __init__(self, column_builder: ColumnDataBuilder):
        """Initialize builder"""
        self._column_builder = column_builder
        self._columns: OrderedDict[CliTableColumn, List[str]] | None = None

    def build_data(self, column_names: List[CliTableColumn]) -> Self:
        """Build column data"""
        for name in column_names:
            self._column_builder.building_methods[name.value]()
        self._columns = self._column_builder.columns
        return self

    @property
    def rows(self) -> List[List[Any]]:
        """Transform data into rows"""
        return list(zip(*self._columns.values()))

    @property
    def columns(self) -> OrderedDict[CliTableColumn, List[str]] | None:
        """Return _columns property"""
        return self._columns
