"""Rows painter builder"""
from typing import List, Self, Any
from app_types.dataclasses import NumberColumnColorCondition
from builders.color_pipeline_builder import ColorPipelineBuilder
from enums.columns import CliTableColumn


class TablePainterBuilder:
    """Paint data in table"""
    def __init__(
            self,
            column_names: List[CliTableColumn],
            rows: List[List[Any]],
            number_color_builder: ColorPipelineBuilder,
    ):
        """Constructor"""
        self._column_names = column_names
        self._rows = [[*row] for row in rows]
        self._number_color_builder = number_color_builder

    def set_number_column_color(
            self,
            column_name: CliTableColumn,
            color_conditions: List[NumberColumnColorCondition],
    ) -> Self:
        """Set color for number column"""
        for condition in color_conditions:
            if condition.end is not None:
                self._number_color_builder.range(condition.start, condition.end, condition.color)
            else:
                self._number_color_builder.from_value(condition.start, condition.color)
        pipe = self._number_color_builder.as_pipe()

        index = self._column_names.index(column_name)
        for row in self._rows:
            row[index] = pipe(row[index])

        return self

    @property
    def rows(self):
        """Property accessor for rows"""
        return self._rows
