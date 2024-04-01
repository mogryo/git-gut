"""Test TablePainterBuilder"""
from app_types.dataclasses import NumberColumnColorCondition
from builders.color_pipeline_builder import ColorPipelineBuilder
from builders.table_painter_builder import TablePainterBuilder
from enums.columns import CliTableColumn, CliTableColumnColor


def test_set_manually_color_condition() -> None:
    """Test single column color condition is applied"""
    rows = TablePainterBuilder(
        [CliTableColumn.LINE_COUNT],
        [[1], [10], [20]],
        ColorPipelineBuilder(),
    ).set_number_column_color(
        CliTableColumn.LINE_COUNT,
        [
            NumberColumnColorCondition(0, 5, CliTableColumnColor.GREEN),
            NumberColumnColorCondition(5, None, CliTableColumnColor.YELLOW),
        ],
    ).rows

    assert str(rows[0][0]).find(CliTableColumnColor.GREEN.value) >= 0
    assert str(rows[1][0]).find(CliTableColumnColor.YELLOW.value) >= 0


def test_build_colors() -> None:
    """Test build_colors correctly is applied"""
    rows = TablePainterBuilder(
        [CliTableColumn.LINE_COUNT],
        [[1], [10], [20]],
        ColorPipelineBuilder(),
    ).build_colors({
        CliTableColumn.LINE_COUNT: [
            NumberColumnColorCondition(0, 5, CliTableColumnColor.GREEN),
            NumberColumnColorCondition(5, None, CliTableColumnColor.YELLOW),
        ]
    }).rows

    assert str(rows[0][0]).find(CliTableColumnColor.GREEN.value) >= 0
    assert str(rows[1][0]).find(CliTableColumnColor.YELLOW.value) >= 0
