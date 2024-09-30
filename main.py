"""Main file of application"""

import sys
from typing import Optional, Tuple, List, Dict
import click
from git import Repo, Git, exc
from prettytable import PrettyTable
from sqlalchemy.orm import Session
from sqlalchemy import Engine, Result

from app_types.dataclasses import FileCommitStats, GitLogOptions, SeparateOptionsAsQuery
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
from utils.cli_table import draw_flat_tree_table
from utils.command_option_parser import (
    parse_option_color,
    parse_option_query,
    parse_separate_options_into_query,
)
from utils.git_utils import (
    get_non_text_files,
    get_all_files_stats,
    get_flat_file_tree,
)
from utils.database import create_db_engine, create_tables
from repositories.git_stat_repo import (
    prepare_all_rows,
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

    if process_terminating_options(file_path, nontext):
        return

    engine = create_db_engine()
    create_tables(engine)

    input_query = (
        query
        if query is not None and query.strip() != ""
        else parse_separate_options_into_query(
            SeparateOptionsAsQuery(columns, file_path, sort, filters, since, until)
        )
    )
    column_names, result_rows = process_query(input_query, engine)

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
