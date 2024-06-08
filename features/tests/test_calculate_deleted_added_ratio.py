"""Test calculate_deleted_added_ratio"""

from statistics import StatisticsError
import pytest
from app_types.dataclasses import FileCommitStats
from features.technical_debt import calculate_deleted_added_ratio


def test_empty_list() -> None:
    """Test empty commit stat list, should throw error"""
    with pytest.raises(StatisticsError):
        calculate_deleted_added_ratio([])


def test_zero_added_value() -> None:
    """Test zero value in added lines - should be replaced to 1"""
    assert (
        calculate_deleted_added_ratio(
            [
                FileCommitStats(added_lines=0, removed_lines=5, author=""),
            ]
        )
        == 5
    )


def test_zero_deleted_value() -> None:
    """Test zero value in deleted lines - should be replaced to 1"""
    assert (
        calculate_deleted_added_ratio(
            [
                FileCommitStats(added_lines=5, removed_lines=0, author=""),
            ]
        )
        == 0
    )


def test_valid_multiple_stats() -> None:
    """Test valid stats - should calculate result"""
    assert (
        calculate_deleted_added_ratio(
            [
                FileCommitStats(10, 5, ""),
                FileCommitStats(20, 10, ""),
                FileCommitStats(30, 15, ""),
            ]
        )
        == 0.5
    )


def test_result_is_harmonic_mean() -> None:
    """Test that result is harmonic mean"""
    result = calculate_deleted_added_ratio(
        [
            FileCommitStats(1, 2, ""),
            FileCommitStats(1, 5, ""),
            FileCommitStats(1, 7, ""),
            FileCommitStats(1, 9, ""),
        ]
    )
    assert f"{result:.2f}" == "5.75"
