"""Main file of application"""

from typing import Optional, Tuple
import click

from app_types.dataclasses import SeparateOptionsAsQuery
from command_interface.option_processors import (
    process_execute_stored_query,
    process_query,
    process_save_query,
    process_terminating_options,
)
from command_interface.options import (
    columns_option,
    since_option,
    sort_option,
    filter_option,
    query_option,
    non_text_files_option,
    until_option,
    table_option,
    save_query_option,
    execute_stored_query_option,
    show_stored_queries_option,
    remove_stored_query,
)
from utils.cli_table import draw_flat_tree_table, create_table_instance
from utils.command_option_parser import parse_separate_options_into_query
from utils.database import create_db_engine, create_tables
from validators.command_option_validators import assert_correct_table_library


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
@save_query_option
@execute_stored_query_option
@show_stored_queries_option
@remove_stored_query
# pylint: disable = too-many-arguments
# pylint: disable = too-many-locals
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
    save_query: Optional[str],
    execute_query: Optional[str],
    list_queries: Optional[bool],
    remove_query: Optional[str],
):
    """Command entry point"""
    file_path: str = file_paths[0] if len(file_paths) > 0 else "./"

    if process_terminating_options(
        file_path,
        list_queries=list_queries,
        remove_queries=remove_query,
        list_non_text=nontext,
    ):
        return

    engine = create_db_engine()
    create_tables(engine)

    input_query: str
    if (stored_query := process_execute_stored_query(execute_query)) is not None:
        input_query = stored_query
    elif query is not None and query.strip() != "":
        input_query = query
    else:
        input_query = parse_separate_options_into_query(
            SeparateOptionsAsQuery(columns, file_path, sort, filters, since, until)
        )

    column_names, result_rows = process_query(input_query, engine)

    table_lib_result = create_table_instance(table)
    assert_correct_table_library(table_lib_result)
    draw_flat_tree_table(column_names, result_rows, table_lib_result.value)
    print(f"Total files: {len(result_rows)}")

    process_save_query(query, save_query)


if __name__ == "__main__":
    # pylint: disable = no-value-for-parameter
    git_hot()
