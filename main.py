"""Main file of application"""

from typing import Optional, Tuple, List, Dict
import click
from git import Repo, Git
from sqlalchemy.orm import Session
from sqlalchemy import Engine

from app_types.dataclasses import FileCommitStats, GitLogOptions, SeparateOptionsAsQuery
from app_types.result import ResultUnion
from builders.column_data_builder import ColumnDataBuilder
from builders.table_data_builder import TableDataBuilder
from command_interface.options import (
    columns_option,
    since_option,
    sort_option,
    filter_option,
    query_option,
    non_text_files_option,
    until_option,
    table_option,
)
from enums.table import CliTableColumn
from utils.cli_table import draw_flat_tree_table, create_table_instance
from utils.command_option_parser import (
    parse_option_query,
    parse_separate_options_into_query,
)
from utils.git_utils import (
    get_non_text_files,
    get_all_files_stats,
    get_flat_file_tree,
    get_repo_instance,
)
from utils.database import create_db_engine, create_tables
from repositories.git_stat_repo import (
    prepare_all_rows,
    prepare_query_statement,
)
from validators.command_option_validators import assert_correct_table_library
from validators.repo_validators import assert_repo_result_is_valid
from validators.root_node_validators import assert_root_node_result_is_valid


def process_query(
    query: Optional[str],
    engine: Engine,
) -> Tuple[List[CliTableColumn], List[List[str | float | int]]]:
    """Process query option provided"""
    all_files_stats: Dict[str, List[FileCommitStats]]
    root_node_result = parse_option_query(query)

    assert_root_node_result_is_valid(root_node_result)
    root_node = root_node_result.value

    repo_result: ResultUnion[Repo] = get_repo_instance(root_node.from_node.path)
    assert_repo_result_is_valid(repo_result)
    repo: Repo = repo_result.value

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
        rows = [[*row] for row in session.execute(select)]

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
@filter_option
@query_option
@non_text_files_option
@since_option
@until_option
@table_option
# pylint: disable = too-many-arguments
def git_hot(
    file_paths: Tuple[str],
    columns: Optional[str],
    sort: Optional[str],
    filters: Optional[str],
    query: Optional[str],
    nontext: bool,
    since: Optional[str],
    until: Optional[str],
    table: Optional[str],
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

    table_lib_result = create_table_instance(table)
    assert_correct_table_library(table_lib_result)
    draw_flat_tree_table(column_names, result_rows, table_lib_result.value)
    print(f"Total files: {len(result_rows)}")


if __name__ == "__main__":
    # pylint: disable = no-value-for-parameter
    git_hot()
