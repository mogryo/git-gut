"""Functions to calculate different technical debt levels"""
from typing import List
from statistics import mean
from app_types.utils import FileCommitStats


def calculate_deleted_added_ratio(commit_stats: List[FileCommitStats]) -> float:
    """Calculates ratio: deleted lines/added lines"""
    def parse_zero(number: int) -> int:
        """Local function to replace zero as 1"""
        return number if number != 0 else 1

    added_deleted_ratios = [
        info.removed_lines / parse_zero(info.added_lines) for info in commit_stats
    ]
    return mean(added_deleted_ratios)


def calculate_line_count(commit_stats: List[FileCommitStats]) -> int:
    """Calculates total lines of code in file, based on added and deleted per commit"""
    return sum(info.added_lines - info.removed_lines for info in commit_stats)
