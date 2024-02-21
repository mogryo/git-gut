from typing import Unpack
from git import Repo, Git
from prettytable import PrettyTable
from app_types import DrawFlatTreeTableKwargs, CliTableColumnLabel
from builders.ColumnBuilder import ColumnBuilder


def draw_flat_tree_table(repo: Repo, git_instance: Git, **kwargs: Unpack[DrawFlatTreeTableKwargs]) -> None:
    column_technical_names = kwargs.get("columns")

    rows = ColumnBuilder(git_instance, repo, pathname_length=kwargs.get("pathname_length", 2))\
        .build_from_column_names(column_technical_names)\
        .result()

    table = kwargs.get(
        "cli_table",
        PrettyTable(list(map(lambda x: CliTableColumnLabel[x].value, column_technical_names)))
    )
    for row in rows:
        table.add_row(row)

    print(table)
