"""Builder pattern for columns"""
from typing import Unpack, List, Self, Callable, Dict
from collections import OrderedDict
from git import Git, Repo
from app_types.utils import ColumnBuilderKwargs
from decorators.column_building_method import column_building_method
from enums.columns import CliTableColumn
from utils.git_utils import get_flat_file_tree, get_file_stats, get_most_frequent_author,\
    get_top_author_by_stat
from utils.filesystem import trim_directories
from features.technical_debt import calculate_deleted_added_ratio, calculate_line_count


class ColumnDataBuilder:
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

    @column_building_method(CliTableColumn.FILE_NAME)
    def add_file_name(self) -> Self:
        """Add file name column"""
        self._columns[CliTableColumn.FILE_NAME.value] = [
            trim_directories(name, self.pathname_length) for name in self.flat_file_tree
        ]

        return self

    @column_building_method(CliTableColumn.COMMIT_AMOUNT)
    def add_commit_amount(self) -> Self:
        """Add commit amount column"""
        self._columns[CliTableColumn.COMMIT_AMOUNT.value] = [
            str(len(get_file_stats(self.git_instance, name))) for name in self.flat_file_tree
        ]

        return self

    @column_building_method(CliTableColumn.MOST_FREQUENT_AUTHOR)
    def add_author(self) -> Self:
        """Add author column"""
        self._columns[CliTableColumn.MOST_FREQUENT_AUTHOR.value] = list(
            map(lambda x: get_most_frequent_author(self.git_instance, x), self.flat_file_tree)
        )

        return self

    @column_building_method(CliTableColumn.MOST_ADDED_AUTHOR)
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

    @column_building_method(CliTableColumn.MOST_DELETED_AUTHOR)
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

    @column_building_method(CliTableColumn.DELETED_ADDED_RATIO)
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

    @column_building_method(CliTableColumn.LINE_COUNT)
    def add_line_count(self) -> Self:
        """Add line amount in file (from git history) column"""
        self._columns[CliTableColumn.LINE_COUNT.value] = list(map(
            lambda file_name: str(calculate_line_count(
                get_file_stats(self.git_instance, file_name)
            )),
            self.flat_file_tree
        ))

        return self

    @property
    def building_methods(self) -> Dict[str, Callable[[], Self]]:
        """Get all methods for building column data"""
        def is_builder_method(method_name: str):
            """Determine if method is column builder method"""
            return not method_name.startswith('_') and method_name != 'building_methods'\
                and method_name != 'git_instance'\
                and hasattr(getattr(self, method_name), "builder_column_name")\
                and getattr(self, method_name).builder_column_name

        builder_methods = list(filter(is_builder_method, dir(self)))

        return {
            getattr(self, func_name)
            .builder_column_name.value: getattr(self, func_name) for func_name in builder_methods
        }

    @property
    def columns(self) -> OrderedDict[str, List[str]]:
        """Return columns, and reset builder"""
        return self._columns
