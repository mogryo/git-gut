"""Main file of application"""

import sys
from typing import Optional, Tuple, List, Dict
import click
from git import Repo, Git, exc
from prettytable import PrettyTable
from sqlalchemy.orm import Session
from sqlalchemy import Engine, Result

from app_types.dataclasses import FileCommitStats, GitLogOptions
from builders.color_pipeline_builder import ColorPipelineBuilder
from builders.column_data_builder import ColumnDataBuilder
from builders.table_data_builder import TableDataBuilder
from builders.table_painter_builder import TablePainterBuilder
from command_interface.options import (
    columns_option,
    since_otion,
    sort_option,
    colors_option,
    filter_option,
    query_option,
    non_text_files_option,
    until_option,
)
from enums.columns import CliTableColumn
from query_option_parser.parser import parse_where_statement
from utils.cli_table import draw_flat_tree_table
from utils.command_option_parser import (
    parse_option_columns,
    parse_option_sort,
    parse_option_color,
    parse_option_query,
)
from utils.git_utils import (
    get_non_text_files,
    get_all_files_stats,
    get_flat_file_tree,
)
from utils.database import create_db_engine, create_tables
from repositories.git_stat_repo import (
    prepare_all_rows,
    prepare_select,
    prepare_order_by,
    prepare_where,
    prepare_query_statement,
)


def process_query(
    query: Optional[str],
    engine: Engine,
) -> Tuple[List[CliTableColumn], Result]:
    """Process query option provided"""
    all_files_stats: Dict[str, List[FileCommitStats]]
    root_node = parse_option_query(query)

    if root_node.from_node is None:
        print("FROM path was not provided")
        sys.exit()
    if root_node.show_node is None:
        print("SHOW columns are not valid")
        sys.exit()

    repo: Repo
    try:
        repo = Repo(root_node.from_node.path, search_parent_directories=True)
    except exc.InvalidGitRepositoryError:
        print("Provided FROM path is not GIT repository")
        sys.exit()

    flat_file_tree = get_flat_file_tree(
        repo.head.commit.tree,
        root_node.from_node.path,
    )
    all_files_stats = get_all_files_stats(
        flat_file_tree,
        repo.git,
        GitLogOptions(
            (
                root_node.interval_node.since
                if root_node.interval_node is not None
                else None
            ),
            (
                root_node.interval_node.until
                if root_node.interval_node is not None
                else None
            ),
        ),
    )

    table_data_builder = TableDataBuilder(
        ColumnDataBuilder(
            all_files_stats,
            flat_file_tree,
            repo,
            pathname_length=2,
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


# pylint: disable = too-many-arguments
# pylint: disable = too-many-locals
def process_separate_options(
    columns: Optional[str],
    sort: Optional[str],
    filters: Optional[str],
    log_options: GitLogOptions,
    engine: Engine,
    file_path: str,
) -> Tuple[List[CliTableColumn], Result]:
    """Process separate options: columns, sort, filters"""
    repo: Repo
    try:
        repo = Repo(file_path, search_parent_directories=True)
    except exc.InvalidGitRepositoryError:
        print("Provided FROM path is not GIT repository")
        sys.exit()

    flat_file_tree = get_flat_file_tree(
        repo.head.commit.tree,
        file_path,
    )

    all_files_stats = get_all_files_stats(
        flat_file_tree,
        repo.git,
        log_options,
    )

    table_data_builder = TableDataBuilder(
        ColumnDataBuilder(all_files_stats, flat_file_tree, repo, pathname_length=2)
    )
    column_names = parse_option_columns(columns if columns is not None else "")
    data_rows = table_data_builder.build_data(column_names).rows

    with Session(engine) as session:
        git_stat_list = prepare_all_rows(column_names, data_rows)
        session.add_all(git_stat_list)
        session.commit()

        select_statement = prepare_select(column_names)
        select_statement = prepare_order_by(parse_option_sort(sort), select_statement)
        select_statement = prepare_where(
            parse_where_statement(filters), select_statement
        )

        sorted_rows = session.execute(select_statement)

    return column_names, sorted_rows


def process_terminating_options(repo_path: str | None, non_text: bool) -> bool:
    """Process options, after which all other options are ignored"""
    if non_text:
        non_text_files = get_non_text_files(Git(repo_path))
        if len(non_text_files) > 0:
            print("Non-text files:")
            print("\n".join(non_text_files))
        else:
            print("No non-text files have been found!")
        return True

    return False


@click.command()
@click.argument("file_paths", nargs=-1)
@columns_option
@sort_option
@colors_option
@filter_option
@query_option
@non_text_files_option
@since_otion
@until_option
# pylint: disable = too-many-arguments
def git_hot(
    file_paths: Tuple[str],
    columns: Optional[str],
    sort: Optional[str],
    colors: Optional[str],
    filters: Optional[str],
    query: Optional[str],
    nontext: bool,
    since: Optional[str],
    until: Optional[str],
):
    """Command entry point"""
    file_path: str = file_paths[0] if len(file_paths) > 0 else "./"

    is_terminated = process_terminating_options(file_path, nontext)
    if is_terminated:
        return

    engine = create_db_engine()
    create_tables(engine)
    log_options = GitLogOptions(since, until)

    column_names, result_rows = (
        process_query(query, engine)
        if query is not None and query.strip() != ""
        else process_separate_options(
            columns, sort, filters, log_options, engine, file_path
        )
    )

    painted_rows = (
        TablePainterBuilder(
            column_names, [[*row] for row in result_rows], ColorPipelineBuilder()
        )
        .build_colors(parse_option_color(colors))
        .rows
    )

    draw_flat_tree_table(column_names, painted_rows, PrettyTable())
    print(f"Total files: {len(painted_rows)}")


if __name__ == "__main__":
    # pylint: disable = no-value-for-parameter
    git_hot()
