"""Builder for table"""

from typing import List, Dict, Unpack, Callable
from app_types.dataclasses import FileCommitStats
from app_types.utils import ColumnBuilderKwargs
from enums.table import CliTableColumn
from features.technical_debt import calculate_deleted_added_ratio, calculate_line_count
from utils.filesystem import trim_directories
from utils.git_utils import get_most_frequent_author, get_top_author_by_stat


# pylint: disable = too-few-public-methods
class TableDataCalculator:
    """Calculator for table data"""

    def __init__(
        self,
        flat_file_tree: List[str],
        files_stats: Dict[str, List[FileCommitStats]],
        **kwargs: Unpack[ColumnBuilderKwargs],
    ):
        """Initialize calculator"""
        self._flat_file_tree = flat_file_tree
        self._files_stats = files_stats
        self._pathname_length = kwargs.get("pathname_length", 2)
        self._stat_generators: Dict[CliTableColumn, Callable[[str], str]] = {
            CliTableColumn.FILE_NAME: self._add_file_name,
            CliTableColumn.COMMIT_AMOUNT: self._add_commit_amount,
            CliTableColumn.MOST_FREQUENT_AUTHOR: self._add_author,
            CliTableColumn.MOST_ADDED_AUTHOR: self._add_most_added_lines_author,
            CliTableColumn.MOST_DELETED_AUTHOR: self._add_most_deleted_lines_author,
            CliTableColumn.DELETED_ADDED_RATIO: self._add_delete_add_ratio,
            CliTableColumn.LINE_COUNT: self._add_line_count,
        }

    def calculate_data(self, column_names: List[CliTableColumn]) -> List[List[str]]:
        """Calculate table's data"""
        rows = []
        for file_name in self._flat_file_tree:
            row = []
            for name in column_names:
                row.append(self._stat_generators[name](file_name))
            rows.append(row)

        return rows

    def _add_file_name(self, file_name: str) -> str:
        """Calculate file name column"""
        return trim_directories(file_name, self._pathname_length)

    def _add_commit_amount(self, file_name: str) -> str:
        """Calculate commit amount column"""
        return str(len(self._files_stats.get(file_name, [])))

    def _add_author(self, file_name: str) -> str:
        """Calculate author column"""
        return get_most_frequent_author(self._files_stats.get(file_name, []))

    def _add_most_added_lines_author(self, file_name: str) -> str:
        """Calculate author of most added lines of code column"""
        return get_top_author_by_stat(
            self._files_stats.get(file_name, []),
            lambda x: int(x.added_lines),
        )

    def _add_most_deleted_lines_author(self, file_name: str) -> str:
        """Calculate author of most deleted lines of code column"""
        return get_top_author_by_stat(
            self._files_stats.get(file_name, []),
            lambda x: int(x.removed_lines),
        )

    def _add_delete_add_ratio(self, file_name: str) -> str:
        """Calculate deleted/added ratio column"""

        def shorten_ratio(number: float) -> str:
            """Local function to shorten the float precision"""
            return f"{number:.4f}"

        return shorten_ratio(
            calculate_deleted_added_ratio(self._files_stats.get(file_name, []))
        )

    def _add_line_count(self, file_name: str) -> str:
        """Calculate line amount in file (from git history) column"""
        return str(calculate_line_count(self._files_stats.get(file_name, [])))
