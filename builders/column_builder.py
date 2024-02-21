"""Builder pattern for columns"""
from typing import Unpack, Any, List, Self
from git import Git, Repo
from app_types.utils import ColumnBuilderKwargs, CliTableColumn
from utils.git_utils import get_flat_file_tree, get_file_stats
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

    def as_rows(self) -> List[List[Any]]:
        """Transform data into rows"""
        return list(zip(*self._columns))

    def build_from_column_names(self, column_names: List[CliTableColumn]) -> Self:
        """Build columns/rows form column names"""
        for name in column_names:
            self._methods[name]()
        return self
