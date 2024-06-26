"""Git utils"""

from typing import List, Callable
from functools import cache
from statistics import mode
from git import Tree, Git
from app_types.dataclasses import FileCommitStats
from utils.numbers import is_number
from utils.text import trim_side_quotes


def get_flat_file_tree(tree: Tree) -> List[str]:
    """
    Iterate through the whole git file tree.
    :param tree: Instance of git.Tree
    :return: Flat representation of file tree.
    """
    generated_list = []
    for entry in tree:
        if entry.type == "blob":
            generated_list.append(entry.path)
        if entry.type == "tree":
            generated_list.extend(get_flat_file_tree(entry))

    return generated_list


def is_stat_trackable(split_stat: List[str]) -> bool:
    """Check if commit stats can be tracked, that is - they are integers"""
    return (
        len(split_stat) >= 2 and is_number(split_stat[0]) and is_number(split_stat[1])
    )


@cache
def get_file_stats(git_instance: Git, filepath: str) -> List[FileCommitStats]:
    """
    Collect number stats about file from git.
    :param git_instance: Instance of git.Git
    :param filepath: File path.
    :return: Return list of stats.
    """
    raw_result: str = git_instance.log(
        "--follow", "--numstat", '--format="%an"', "--", filepath
    )
    separate_lines = list(filter(lambda x: x != "", raw_result.splitlines()))
    commit_list = list(zip(separate_lines[::2], separate_lines[1::2]))

    result = []
    for commit_info in commit_list:
        split_stat = commit_info[1].split()

        if is_stat_trackable(split_stat):
            result.append(
                FileCommitStats(
                    added_lines=int(split_stat[0]),
                    removed_lines=int(split_stat[1]),
                    author=commit_info[0],
                )
            )

    return result


def get_most_frequent_author(git_instance: Git, file_name: str) -> str:
    """
    Calculate the author of the most code in file
    :param git_instance: Instance of git.Git
    :param file_name: Name of file
    :return: Author name
    """
    authors = [info.author for info in get_file_stats(git_instance, file_name)]
    return trim_side_quotes(mode(authors))


def get_top_author_by_stat(
    git_instance: Git, file_name: str, func: Callable[[FileCommitStats], int]
) -> str:
    """
    Functions calculates top author,
    by summing up specific stat which is returned by provided function
    :param git_instance: Instance of git.Git
    :param file_name: Name of file
    :param func: Function to be applied on file commit stats to extract specific property
    :return: Top author and summed up stat
    """
    authors_data = {}
    for stat in get_file_stats(git_instance, file_name):
        authors_data[stat.author] = authors_data.get(stat.author, 0) + func(stat)

    top_author = max(authors_data, key=authors_data.get)
    author_total_sum = authors_data[top_author]

    return f"{trim_side_quotes(top_author)} ({author_total_sum})"


def get_non_text_files(git_instance: Git) -> List[str]:
    """
    Get GIT tracked files which are non text (binary).
    :param git_instance: Instance of git.Git
    :param filepath: File path.
    :return: List of file names.
    """
    existing_files: List[str] = git_instance.ls_files().split()
    result: List[str] = []

    for existing_file in existing_files:
        log_result: str = git_instance.log(
            "--follow", "--numstat", '--format="%an"', "-n 1", "--", existing_file
        )
        separate_lines = list(
            filter(
                lambda x: x != "" and not x.startswith('"'),
                log_result.splitlines(),
            )
        )

        for commit_info in separate_lines:
            split_stat = commit_info.split()

            if not is_stat_trackable(split_stat):
                result.append(existing_file)

    return result
