"""Main file of application"""
from typing import Optional
import click
from git import Repo, Git
from prettytable import PrettyTable
from sqlalchemy.orm import Session

from builders.color_pipeline_builder import ColorPipelineBuilder
from builders.column_data_builder import ColumnDataBuilder
from builders.table_data_builder import TableDataBuilder
from builders.table_painter_builder import TablePainterBuilder
from defaults.color import LINE_COUNT_COLOR, DELETE_ADD_RATIO_COLOR
from defaults.command import DEFAULT_COLUMNS, DEFAULT_SORT
from utils.cli_table import draw_flat_tree_table
from utils.command_option_parser import parse_option_columns, parse_option_sort
from utils.database import create_db_engine, create_tables
from enums.columns import CliTableColumn
from repositories.git_stat_repo import prepare_all_rows, prepare_select,\
    prepare_order_by

COMMAND_OPTION_COLUMN_NAMES = list(filter(lambda x: not x.startswith('_'), dir(CliTableColumn)))
COLUMN_OPTION_EXAMPLE = f"{CliTableColumn.FILE_NAME.value},{CliTableColumn.LINE_COUNT.value}"
SORT_OPTION_EXAMPLE = f"{CliTableColumn.FILE_NAME.value}-asc," \
    f"{CliTableColumn.LINE_COUNT.value}-desc"


@click.command()
@click.argument('repo_path')
@click.option(
    "--columns",
    default=DEFAULT_COLUMNS,
    help=f"""
        Column names: ${COMMAND_OPTION_COLUMN_NAMES}
        Example of input: --columns={COLUMN_OPTION_EXAMPLE}
    """
)
@click.option(
    "--sort",
    default=DEFAULT_SORT,
    help=f"""
        Column names: ${COMMAND_OPTION_COLUMN_NAMES}
        Sort variants: asc or desc
        Example of input: --sort={SORT_OPTION_EXAMPLE}
    """
)
def git_hot(repo_path: str, columns: Optional[str], sort: Optional[str]):
    """Command entry point"""
    engine = create_db_engine()
    create_tables(engine)
    repo = Repo(repo_path)
    git_instance = Git(repo_path)
    column_names = parse_option_columns(columns)
    sort_rules = parse_option_sort(sort)

    data_rows = TableDataBuilder(ColumnDataBuilder(git_instance, repo, pathname_length=2))\
        .build_data(column_names)\
        .rows

    with Session(engine) as session:
        git_stat_list = prepare_all_rows(column_names, data_rows)
        session.add_all(git_stat_list)
        session.commit()

        select_statement = prepare_select(column_names)
        select_statement = prepare_order_by(sort_rules, select_statement)

        sorted_rows = session.execute(select_statement)

    painted_rows = TablePainterBuilder(
        column_names, [[*row] for row in sorted_rows], ColorPipelineBuilder()
    )\
        .set_number_column_color(CliTableColumn.LINE_COUNT, LINE_COUNT_COLOR)\
        .set_number_column_color(CliTableColumn.DELETED_ADDED_RATIO, DELETE_ADD_RATIO_COLOR)\
        .rows

    draw_flat_tree_table(column_names, painted_rows, PrettyTable())
    print(f"Total files: {len(painted_rows)}")


if __name__ == '__main__':
    # pylint: disable = no-value-for-parameter
    git_hot()
