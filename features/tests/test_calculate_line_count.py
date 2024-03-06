"""Test calculate_line_count"""
from features.technical_debt import calculate_line_count
from app_types.utils import FileCommitStats


def test_empty_list() -> None:
    """Test empty list - results in zero"""
    assert calculate_line_count([]) == 0


def test_more_lines_deleted() -> None:
    """Test when more lines deleted"""
    assert calculate_line_count([
        FileCommitStats(10, 100, ""), FileCommitStats(10, 50, "")
    ]) == -130


def test_more_lines_added() -> None:
    """Test when more lines deleted"""
    assert calculate_line_count([
        FileCommitStats(100, 5, ""), FileCommitStats(10, 5, "")
    ]) == 100
