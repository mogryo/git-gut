"""Git utils"""

import asyncio
import os
from typing import List, Callable, Dict, cast, Optional
from statistics import mode
from git import Tree, Git
from app_types.dataclasses import FileCommitStats
from utils.numbers import is_number
from utils.text import trim_side_quotes


CONCURRENT_CONSUMER_AMOUNT = 4


# pylint: disable = too-few-public-methods
class _QueueEnd:
    """
    Class to mark the end of queue
    This class should not be used directly
    """


async def _file_name_producer(queue: asyncio.Queue, file_names: List[str]) -> None:
    """
    Producer for collecting files git stats
    This function should not be called directly
    :param queue: asyncion.Queue
    :param file_names: List of all file names
    :return: Explicitly return None
    """
    for name in file_names:
        await queue.put(name)

    for _ in range(0, CONCURRENT_CONSUMER_AMOUNT):
        await queue.put(_QueueEnd())

    return None


async def _file_name_consumer(
    queue: asyncio.Queue, git_instance: Git
) -> Dict[str, List[FileCommitStats]]:
    """
    Consumer function for collecting files git stats
    This function should not be called directly
    :param queue: asyncio.Queue
    :param git_instance: Git instance
    :return: Returns dictionary, with portion of files and corresponding list of file stats
    """
    result_data: Dict[str, List[FileCommitStats]] = {}
    while True:
        file_name: str | _QueueEnd = await queue.get()
        if isinstance(file_name, _QueueEnd):
            queue.task_done()
            break

        res = await asyncio.to_thread(lambda: get_file_stats(git_instance, file_name))
        result_data[file_name] = res
        queue.task_done()
    return result_data


async def _collect_stats_all_files(git_instance: Git, file_names: List[str]):
    """
    Collect git stats for each file
    This function should not be called directly
    :param git_instance: Instance of Git
    :oaram file_names: List of all file names
    """
    queue = asyncio.Queue(maxsize=32)
    task_result = await asyncio.gather(
        _file_name_producer(queue, file_names),
        *(
            _file_name_consumer(queue, git_instance)
            for _ in range(0, CONCURRENT_CONSUMER_AMOUNT)
        ),
        return_exceptions=True,
    )
    map_result: Dict[str, List[FileCommitStats]] = {}
    for entry in task_result:
        if entry is not None and not isinstance(entry, BaseException):
            map_result |= entry

    return map_result


def get_all_files_stats(
    repo_path: str,
    file_names: List[str],
    git: Git,
) -> Dict[str, List[FileCommitStats]]:
    """
    Return git stats for all specified files
    :param repo_path: Path to git repo
    :param file_names: All specified file names for which we need to collect stats
    :return: List of git stats for each file
    """
    return asyncio.run(_collect_stats_all_files(git, file_names))


def get_flat_file_tree(tree: Tree, specific_path: Optional[str] = None) -> List[str]:
    """
    Iterate through the whole git file tree.
    :param tree: Instance of git.Tree
    :return: Flat representation of file tree.
    """
    if specific_path is not None and os.path.isdir(specific_path):
        return get_sub_directory_file_list(tree, specific_path)

    if specific_path is not None and os.path.isfile(specific_path):
        return get_specific_file_as_list(tree, specific_path)

    return get_tree_file_list(tree)


def get_specific_file_as_list(tree: Tree, specific_path: str) -> List[str]:
    generated_list: List[str] = []
    abs_specific_path = os.path.abspath(specific_path)

    for entry in tree:
        if entry.type == "blob" and entry.abspath == abs_specific_path:
            return [specific_path]
        elif entry.type == "tree":
            generated_list.extend(
                get_specific_file_as_list(cast(Tree, entry), specific_path)
            )

    return generated_list


def get_sub_directory_file_list(tree: Tree, specific_path: str) -> List[str]:
    generated_list: List[str] = []
    abs_specific_path = os.path.abspath(specific_path)

    if tree.abspath == abs_specific_path:
        return get_tree_file_list(tree)

    for entry in tree:
        if entry.abspath == abs_specific_path:
            return get_tree_file_list(cast(Tree, entry))
        elif entry.type == "tree":
            generated_list.extend(
                get_sub_directory_file_list(cast(Tree, entry), specific_path)
            )

    return generated_list


def get_tree_file_list(tree: Tree) -> List[str]:
    """
    Iterate through the whole git file tree.
    :param tree: Instance of git.Tree
    :return: Flat representation of file tree.
    """
    generated_list: List[str] = []

    for entry in tree:
        if entry.type == "blob":
            generated_list.append(cast(str, entry.path))
        if entry.type == "tree":
            generated_list.extend(get_flat_file_tree(entry))

    return generated_list


def is_stat_trackable(split_stat: List[str]) -> bool:
    """Check if commit stats can be tracked, that is - they are integers"""
    return (
        len(split_stat) >= 2 and is_number(split_stat[0]) and is_number(split_stat[1])
    )


def get_file_stats(git_instance: Git, filepath: str) -> List[FileCommitStats]:
    """
    Collect number stats about single file from git.
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


def get_most_frequent_author(
    file_name: str, files_stats: Dict[str, List[FileCommitStats]]
) -> str:
    """
    Calculate the author of the most code in file
    :param git_instance: Instance of git.Git
    :param file_name: Name of file
    :return: Author name
    """
    authors = [info.author for info in files_stats.get(file_name, [])]
    return trim_side_quotes(mode(authors))


def get_top_author_by_stat(
    file_name: str,
    files_stats: Dict[str, List[FileCommitStats]],
    func: Callable[[FileCommitStats], int],
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
    for stat in files_stats.get(file_name, []):
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
