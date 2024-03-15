"""Builder pattern for columns"""
from typing import Unpack, Any, List, Self, Callable
from collections import OrderedDict
from git import Git, Repo
from app_types.utils import ColumnBuilderKwargs, CliTableColumn
from utils.git_utils import get_flat_file_tree, get_file_stats, get_most_frequent_author,\
    get_top_author_by_stat
from utils.filesystem import trim_directories
from utils.id_generator import generate_unique_keys
from features.technical_debt import calculate_deleted_added_ratio, calculate_line_count


class ColumnBuilder:
    """Builder for columns"""
    def __init__(
            self,
            git_instance: Git,
            repo_instance: Repo,
            **kwargs: Unpack[ColumnBuilderKwargs]
    ):
        self.git_instance = git_instance
        self.repo_instance = repo_instance
        self.flat_file_tree = get_flat_file_tree(self.repo_instance.head.commit.tree)
        self.pathname_length = kwargs.get("pathname_length", 2)
        self._columns: OrderedDict[str, List[str]] = OrderedDict()
        self._methods = {
            CliTableColumn.ID.value: self.add_id,
            CliTableColumn.FILE_NAME.value: self.add_file_name,
            CliTableColumn.COMMIT_AMOUNT.value: self.add_commit_amount,
            CliTableColumn.MOST_FREQUENT_AUTHOR.value: self.add_author,
            CliTableColumn.MOST_ADDED_AUTHOR.value: self.add_most_added_lines_author,
            CliTableColumn.MOST_DELETED_AUTHOR.value: self.add_most_deleted_lines_author,
            CliTableColumn.DELETED_ADDED_RATIO.value: self.add_delete_add_ratio,
            CliTableColumn.LINE_COUNT.value: self.add_line_count,
        }

    def add_id(self) -> Self:
        """Add ID column"""
        self._columns[CliTableColumn.ID.value] = generate_unique_keys(
            start_key=0,
            end_key=len(self.flat_file_tree),
            key_length=len(str(len(self.flat_file_tree)))
        )

        return self

    def add_file_name(self) -> Self:
        """Add file name column"""
        self._columns[CliTableColumn.FILE_NAME.value] = [
            trim_directories(name, self.pathname_length) for name in self.flat_file_tree
        ]

        return self

    def add_commit_amount(self) -> Self:
        """Add commit amount column"""
        self._columns[CliTableColumn.COMMIT_AMOUNT.value] = [
            str(len(get_file_stats(self.git_instance, name))) for name in self.flat_file_tree
        ]

        return self

    def add_author(self) -> Self:
        """Add author column"""
        self._columns[CliTableColumn.MOST_FREQUENT_AUTHOR.value] = list(
            map(lambda x: get_most_frequent_author(self.git_instance, x), self.flat_file_tree)
        )

        return self

    def add_most_added_lines_author(self) -> Self:
        """Add author of most added lines of code column"""
        self._columns[CliTableColumn.MOST_ADDED_AUTHOR.value] = (
            list(
                map(
                    lambda file_name: get_top_author_by_stat(
                        self.git_instance, file_name, lambda x: int(x.added_lines),
                    ),
                    self.flat_file_tree
                )
            )
        )

        return self

    def add_most_deleted_lines_author(self) -> Self:
        """Add author of most deleted lines of code column"""
        self._columns[CliTableColumn.MOST_DELETED_AUTHOR.value] = list(
            map(
                lambda file_name: get_top_author_by_stat(
                    self.git_instance, file_name, lambda x: int(x.removed_lines),
                ),
                self.flat_file_tree
            )
        )

        return self

    def add_delete_add_ratio(self) -> Self:
        """Add deleted/added ratio column"""
        def shorten_ratio(number: float) -> str:
            """Local function to shorten the float precision"""
            return f"{number:.4f}"

        self._columns[CliTableColumn.DELETED_ADDED_RATIO.value] = list(map(
            lambda file_name: shorten_ratio(calculate_deleted_added_ratio(
                get_file_stats(self.git_instance, file_name)
            )),
            self.flat_file_tree
        ))

        return self

    def add_line_count(self) -> Self:
        """Add line amount in file (from git history) column"""
        self._columns[CliTableColumn.LINE_COUNT.value] = list(map(
            lambda file_name: str(calculate_line_count(
                get_file_stats(self.git_instance, file_name)
            )),
            self.flat_file_tree
        ))

        return self

    def as_rows(self) -> List[List[Any]]:
        """Transform data into rows"""
        return list(zip(*self._columns.values()))

    def build_from_column_names(self, column_names: List[CliTableColumn]) -> Self:
        """Build columns/rows form column names"""
        for name in column_names:
            self._methods[name]()

        return self

    def set_color_pipe(self, column_name: CliTableColumn, pipe: Callable[[str], str]):
        """Apply color pipe for specific column"""
        self._columns[column_name.value] = [
            pipe(value) for value in self._columns[column_name.value]
        ]

        return self
