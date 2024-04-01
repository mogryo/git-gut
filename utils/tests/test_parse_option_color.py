"""Test parse_option_color"""
from app_types.dataclasses import NumberColumnColorCondition
from utils.command_option_parser import parse_option_color
from enums.columns import CliTableColumn


def test_nothing_is_provided() -> None:
    """Test nothing is provided"""
    assert not parse_option_color()


def test_empty_string() -> None:
    """Test empty string provided"""
    assert not parse_option_color("")


def test_omit_end_range() -> None:
    """Test that omitting end range is valid (meaning till infinity)"""
    colors = parse_option_color(
        "daratio-1,,red;"
    )

    assert colors[CliTableColumn.DELETED_ADDED_RATIO][0].end is None


def test_single_color_condition() -> None:
    """Test single condition"""
    colors = parse_option_color(
        "daratio-0,0.15,green/0.15,0.3,yellow/0.3,,red;"
    )

    assert len(colors[CliTableColumn.DELETED_ADDED_RATIO]) == 3
    for condition in colors[CliTableColumn.DELETED_ADDED_RATIO]:
        assert isinstance(condition, NumberColumnColorCondition)


def test_multiple_color_conditions() -> None:
    """Test multiple conditions"""
    colors = parse_option_color(
        "daratio-0,0.15,green/0.15,0.3,yellow/0.3,,red;"
        "linecount-100,200,green/200,300,yellow/300,,red"
    )
    assert len(colors[CliTableColumn.DELETED_ADDED_RATIO]) == 3
    assert len(colors[CliTableColumn.LINE_COUNT]) == 3

    for condition in colors[CliTableColumn.DELETED_ADDED_RATIO]:
        assert isinstance(condition, NumberColumnColorCondition)
    for condition in colors[CliTableColumn.LINE_COUNT]:
        assert isinstance(condition, NumberColumnColorCondition)
