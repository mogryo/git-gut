"""Test _is_color_in_range"""

from utils.colors import _is_color_in_range


def test_none_range_value() -> None:
    """Check when whole range is None value"""
    assert not _is_color_in_range(20, None)


def test_value_is_in_range_with_both_edges() -> None:
    """Check when provided value is in range, start and end is provided"""
    assert _is_color_in_range(20, (0, 30))


def test_value_is_in_range_with_only_start_edge() -> None:
    """Check when provided value is in range, only start is provided"""
    assert _is_color_in_range(20, (10,))


def test_value_is_in_range_with_only_end_edge() -> None:
    """Check when provided value is in range, only end is provided"""
    assert _is_color_in_range(20, (None, 30))


def test_value_is_not_in_range_with_both_edges() -> None:
    """Check when value is not in range, with start and end is provided"""
    assert not _is_color_in_range(40, (0, 30))


def test_value_is_not_in_range_with_only_start_edge() -> None:
    """Check when provided value is not in range, only start is provided"""
    assert not _is_color_in_range(5, (10,))


def test_value_is_not_in_range_with_only_end_edge() -> None:
    """Check when provided value is not in range, only end is provided"""
    assert not _is_color_in_range(40, (None, 30))
