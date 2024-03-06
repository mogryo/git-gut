"""Table functions"""
from typing import Unpack
from git import Repo, Git
from prettytable import PrettyTable
from app_types.utils import DrawFlatTreeTableKwargs, CliTableColumnLabel
from builders.column_builder import ColumnBuilder


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

    rows = ColumnBuilder(git_instance, repo, pathname_length=kwargs.get("pathname_length", 2))\
        .build_from_column_names(column_technical_names)\
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
