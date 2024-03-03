"""Builder pattern for columns"""
from typing import Unpack, Any, List, Self
from git import Git, Repo
from app_types.utils import ColumnBuilderKwargs, CliTableColumn
from utils.git_utils import get_flat_file_tree, get_file_stats, get_most_frequent_author,\
    get_top_author_by_stat
from utils.filesystem import trim_directories
from utils.id_generator import generate_unique_keys


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
        self._columns: List[List[Any]] = []
        self._methods = {
            CliTableColumn.ID.value: self.add_id,
            CliTableColumn.FILE_NAME.value: self.add_file_name,
            CliTableColumn.COMMIT_AMOUNT.value: self.add_commit_amount,
            CliTableColumn.MOST_FREQUENT_AUTHOR.value: self.add_author,
            CliTableColumn.MOST_ADDED_AUTHOR.value: self.add_most_added_lines_author,
            CliTableColumn.MOST_DELETED_AUTHOR.value: self.add_most_deleted_lines_author,
        }

    def add_id(self) -> Self:
        """Add ID column"""
        self._columns.append(
            generate_unique_keys(
                start_key=0,
                end_key=len(self.flat_file_tree),
                key_length=len(str(len(self.flat_file_tree)))
            )
        )
        return self

    def add_file_name(self) -> Self:
        """Add file name column"""
        self._columns.append(
            [trim_directories(name, self.pathname_length) for name in self.flat_file_tree]
        )
        return self

    def add_commit_amount(self) -> Self:
        """Add commit amount column"""
        self._columns.append(
            [len(get_file_stats(self.git_instance, name)) for name in self.flat_file_tree]
        )
        return self

    def add_author(self) -> Self:
        """Add author column"""
        self._columns.append(
            list(
                map(lambda x: get_most_frequent_author(self.git_instance, x), self.flat_file_tree)
            )
        )
        return self

    def add_most_added_lines_author(self) -> Self:
        """Add author of most added lines of code column"""
        self._columns.append(
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
        self._columns.append(
            list(
                map(
                    lambda file_name: get_top_author_by_stat(
                        self.git_instance, file_name, lambda x: int(x.removed_lines),
                    ),
                    self.flat_file_tree
                )
            )
        )
        return self

    def as_rows(self) -> List[List[Any]]:
        """Transform data into rows"""
        return list(zip(*self._columns))

    def build_from_column_names(self, column_names: List[CliTableColumn]) -> Self:
        """Build columns/rows form column names"""
        for name in column_names:
            self._methods[name]()
        return self
