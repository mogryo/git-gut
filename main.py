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
from command_interface.options import columns_option, sort_option, colors_option
from utils.cli_table import draw_flat_tree_table
from utils.command_option_parser import parse_option_columns, parse_option_sort, parse_option_color
from utils.database import create_db_engine, create_tables
from repositories.git_stat_repo import prepare_all_rows, prepare_select,\
    prepare_order_by


@click.command()
@click.argument('repo_path')
@columns_option
@sort_option
@colors_option
def git_hot(repo_path: str, columns: Optional[str], sort: Optional[str], colors: Optional[str]):
    """Command entry point"""
    engine = create_db_engine()
    create_tables(engine)
    column_names = parse_option_columns(columns)

    data_rows = TableDataBuilder(
        ColumnDataBuilder(Git(repo_path), Repo(repo_path), pathname_length=2)
    )\
        .build_data(column_names)\
        .rows

    with Session(engine) as session:
        git_stat_list = prepare_all_rows(column_names, data_rows)
        session.add_all(git_stat_list)
        session.commit()

        select_statement = prepare_select(column_names)
        select_statement = prepare_order_by(parse_option_sort(sort), select_statement)

        sorted_rows = session.execute(select_statement)

    painted_rows = TablePainterBuilder(
        column_names, [[*row] for row in sorted_rows], ColorPipelineBuilder()
    )\
        .build_colors(parse_option_color(colors))\
        .rows

    draw_flat_tree_table(column_names, painted_rows, PrettyTable())
    print(f"Total files: {len(painted_rows)}")


if __name__ == '__main__':
    # pylint: disable = no-value-for-parameter
    git_hot()
