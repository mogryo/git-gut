"""Main file of application"""
from typing import Optional, Tuple, List
import click
from git import Repo, Git
from prettytable import PrettyTable
from sqlalchemy.orm import Session
from sqlalchemy import Engine, Result

from builders.color_pipeline_builder import ColorPipelineBuilder
from builders.column_data_builder import ColumnDataBuilder
from builders.table_data_builder import TableDataBuilder
from builders.table_painter_builder import TablePainterBuilder
from command_interface.options import columns_option, sort_option, colors_option,\
    filter_option, query_option
from enums.columns import CliTableColumn
from query_option_parser.parser import parse_where_statement
from utils.cli_table import draw_flat_tree_table
from utils.command_option_parser import parse_option_columns, parse_option_sort,\
    parse_option_color, parse_option_query
from utils.database import create_db_engine, create_tables
from repositories.git_stat_repo import prepare_all_rows, prepare_select,\
    prepare_order_by, prepare_where, prepare_query_statement


def process_query(
    query: Optional[str],
    engine: Engine,
) -> Tuple[List[CliTableColumn], Result]:
    """Process query option provided"""
    root_node = parse_option_query(query)
    table_data_builder = TableDataBuilder(
        ColumnDataBuilder(
            Git(root_node.from_node.path), Repo(root_node.from_node.path), pathname_length=2
        )
    )
    select = prepare_query_statement(root_node)
    data_rows = table_data_builder.build_data(root_node.show_node.column_names).rows

    with Session(engine) as session:
        git_stat_list = prepare_all_rows(root_node.show_node.column_names, data_rows)
        session.add_all(git_stat_list)
        session.commit()
        rows = session.execute(select)

    return root_node.show_node.column_names, rows


def process_separate_options(
    columns: Optional[str],
    sort: Optional[str],
    filters: Optional[str],
    engine: Engine,
    repo_path: str,
) -> Tuple[List[CliTableColumn], Result]:
    """Process separate options: columns, sort, filters"""
    table_data_builder = TableDataBuilder(
        ColumnDataBuilder(Git(repo_path), Repo(repo_path), pathname_length=2)
    )
    column_names = parse_option_columns(columns)
    data_rows = table_data_builder.build_data(column_names).rows

    with Session(engine) as session:
        git_stat_list = prepare_all_rows(column_names, data_rows)
        session.add_all(git_stat_list)
        session.commit()

        select_statement = prepare_select(column_names)
        select_statement = prepare_order_by(parse_option_sort(sort), select_statement)
        select_statement = prepare_where(parse_where_statement(filters), select_statement)

        sorted_rows = session.execute(select_statement)

    return column_names, sorted_rows


@click.command()
@click.argument('repo_path')
@columns_option
@sort_option
@colors_option
@filter_option
@query_option
# pylint: disable = too-many-arguments
def git_hot(
        repo_path: str,
        columns: Optional[str],
        sort: Optional[str],
        colors: Optional[str],
        filters: Optional[str],
        query: Optional[str],
):
    """Command entry point"""
    engine = create_db_engine()
    create_tables(engine)

    column_names, result_rows = (
        process_query(query, engine)
        if query is not None and query.strip() != ""
        else process_separate_options(columns, sort, filters, engine, repo_path)
    )

    painted_rows = TablePainterBuilder(
        column_names, [[*row] for row in result_rows], ColorPipelineBuilder()
    )\
        .build_colors(parse_option_color(colors))\
        .rows

    draw_flat_tree_table(column_names, painted_rows, PrettyTable())
    print(f"Total files: {len(painted_rows)}")


if __name__ == '__main__':
    # pylint: disable = no-value-for-parameter
    git_hot()
