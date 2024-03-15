"""Test ColorPipelineBuilder class"""
from pytest import raises
from builders.color_pipeline_builder import ColorPipelineBuilder
from enums.columns import CliTableColumnColor


def test_range_incorrect_order() -> None:
    """Check it's impossible to set provide range, when second value is lower than first"""
    with raises(ValueError):
        ColorPipelineBuilder().range(10, 5, CliTableColumnColor.GREEN)


def test_valid_pipe_is_returned_for_one_column() -> None:
    """Check happy pass if single column name is set"""
    pipe = ColorPipelineBuilder()\
        .range(0, 100, CliTableColumnColor.BLUE)\
        .from_value(101, CliTableColumnColor.GREEN)\
        .as_pipe()

    assert pipe("50") == f"{CliTableColumnColor.BLUE.value}50{CliTableColumnColor.RESET.value}"
