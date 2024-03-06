"""Main file of application"""
from typing import AnyStr
import click
from git import Repo, Git
from utils.cli_table import draw_flat_tree_table
from utils.command_option_parser import parse_option_columns
from app_types.utils import CliTableColumn
from config.command_defaults import DEFAULT_COLUMNS


@click.command()
@click.argument('repo_path')
@click.option(
    "--columns",
    default=DEFAULT_COLUMNS,
    help=f"""
        Column names: ${list(filter(lambda x: not x.startswith('_'), dir(CliTableColumn)))}
        Example of input: --columns={CliTableColumn.ID.value}, {CliTableColumn.FILE_NAME.value}
    """
)
def git_hot(repo_path: AnyStr, columns: AnyStr):
    """Command entry point"""
    repo = Repo(repo_path)
    git_instance = Git(repo_path)

    draw_flat_tree_table(repo, git_instance, columns=parse_option_columns(columns))


if __name__ == '__main__':
    # pylint: disable = no-value-for-parameter
    git_hot()
