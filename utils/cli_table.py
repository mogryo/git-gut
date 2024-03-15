"""Table functions"""
from typing import Unpack
from git import Repo, Git
from prettytable import PrettyTable
from app_types.utils import DrawFlatTreeTableKwargs
from enums.columns import CliTableColumnLabel, CliTableColumn
from builders.column_builder import ColumnBuilder
from defaults.color_pipelines import line_count_pipe, delete_add_ratio_pipe


def draw_flat_tree_table(
        repo: Repo,
        git_instance: Git,
        **kwargs: Unpack[DrawFlatTreeTableKwargs],
) -> None:
    """
    Draws basic table of flattened git tree, with specific columns.
    :param repo: The instance of git.Repo
    :param git_instance: The instance of git.Git
    :param kwargs: DrawFlatTreeTableKwargs
    :return: None
    """
    column_technical_names = kwargs.get("columns")

    rows = ColumnBuilder(git_instance, repo, pathname_length=kwargs.get("pathname_length", 2)) \
        .build_from_column_names(column_technical_names) \
        .set_color_pipe(CliTableColumn.LINE_COUNT, line_count_pipe) \
        .set_color_pipe(CliTableColumn.DELETED_ADDED_RATIO, delete_add_ratio_pipe) \
        .as_rows()

    table = kwargs.get(
        "cli_table",
        PrettyTable(
            list(map(lambda x: CliTableColumnLabel[x.upper()].value, column_technical_names))
        )
    )
    for row in rows:
        table.add_row(row)

    print(table)
