"""Defaults for column color pipelines"""
from builders.color_pipeline_builder import ColorPipelineBuilder
from enums.columns import CliTableColumnColor

line_count_pipe = ColorPipelineBuilder()\
    .range(0, 250, CliTableColumnColor.GREEN)\
    .range(250, 400, CliTableColumnColor.YELLOW)\
    .from_value(400, CliTableColumnColor.RED)\
    .as_pipe()

delete_add_ratio_pipe = ColorPipelineBuilder()\
    .range(0, 0.15, CliTableColumnColor.GREEN)\
    .range(0.15, 0.3, CliTableColumnColor.YELLOW)\
    .from_value(0.3, CliTableColumnColor.RED)\
    .as_pipe()
