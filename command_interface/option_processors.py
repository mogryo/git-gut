"""Option processors"""

from typing import Optional, Tuple, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import Engine
from git import Repo, Git

from app_types.result import ResultUnion
from app_types.dataclasses import FileCommitStats, GitLogOptions
from builders.column_data_builder import ColumnDataBuilder
from builders.table_data_builder import TableDataBuilder
from enums.table import CliTableColumn
from repositories.git_stat_repo import prepare_query_statement, prepare_all_rows
from utils.command_option_parser import parse_option_query
from utils.filesystem import get_stored_queries_from_file, save_queries_to_file
from utils.git_utils import (
    get_repo_instance,
    get_flat_file_tree,
    get_all_files_stats,
    get_non_text_files,
)
from validators.command_option_validators import assert_query_exists_for_execution
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


def process_save_query(query: Optional[str], save_query_name: Optional[str]) -> None:
    """Save currently executing query to the file"""
    if query is None or query.strip() == "":
        if save_query_name is not None and save_query_name.strip() != "":
            print(
                "You have provided the query name for saving, but query argument is empty!"
            )
        return

    if save_query_name is None or save_query_name.strip() == "":
        return

    queries = get_stored_queries_from_file()
    queries[save_query_name] = query
    save_queries_to_file(queries)
    print("Query is stored successfully!")


def process_execute_stored_query(query_name: Optional[str]) -> str | None:
    """Execute stored query"""
    if query_name is None or query_name.strip() == "":
        return None

    queries = get_stored_queries_from_file()
    assert_query_exists_for_execution(query_name, queries)

    return queries[query_name]


def process_list_stored_queries(list_queries: Optional[bool]) -> bool:
    """List all the queries if requested"""
    if list_queries:
        queries = get_stored_queries_from_file()

        print("Stored queries")
        for query in queries:
            print(f"{query}: {queries[query]}")

        return True

    return False


def process_remove_stored_query(query_name: Optional[str]) -> bool:
    """Remove previously stored query if requested"""
    if query_name is not None and query_name.strip() != "":
        queries = get_stored_queries_from_file()

        if query_name in queries.keys():
            queries.pop(query_name)
            save_queries_to_file(queries)
            print("Stored query removed successfully")
        else:
            print(
                f"Cannot delete query. There is no stored query with name: {query_name}"
            )

        return True

    return False
