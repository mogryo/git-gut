import click
from typing import AnyStr
from git import Repo, Git
from utils import draw_flat_tree_table, parse_option_columns
from app_types import CliTableColumn


@click.command()
@click.argument('repo_path')
@click.option(
    "--columns",
    default=f"{CliTableColumn.ID.value}, {CliTableColumn.FILE_NAME.value}, {CliTableColumn.COMMIT_AMOUNT.value}",
    help=f"""
        Available column names: ${list(filter(lambda x: not x.startswith('_'), dir(CliTableColumn)))}
        Example of input: --columns={CliTableColumn.ID.value}, {CliTableColumn.FILE_NAME.value}
    """
)
def git_hot(repo_path: AnyStr, columns: AnyStr):
    repo = Repo(repo_path)
    git_instance = Git(repo_path)

    draw_flat_tree_table(repo, git_instance, columns=parse_option_columns(columns))


if __name__ == '__main__':
    git_hot()
