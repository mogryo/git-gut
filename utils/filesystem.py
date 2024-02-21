"""Utils for file names and directories"""
from typing import List
import re


def filter_out_directories(all_files: List[str], exclude_list: List[str]) -> List[str]:
    """
    Filter out not needed directories.
    :param all_files: List of files.
    :param exclude_list: List of paths to exclude.
    :return: List of desired files.
    """
    if (exclude_paths := "|".join(exclude_list)) != "":
        return list(filter(lambda x: not re.search(exclude_paths, x), all_files))

    return [*all_files]


def trim_directories(path: str, required_dir_amount: int) -> str:
    """
    Shorten path of file (how many directories in path), to required length.
    :param path: Path itself.
    :param required_dir_amount: How many directories to leave in the path.
    :return:
    """
    pathname_list = list(filter(lambda split_path: len(split_path) > 0, path.split("/")))
    required_amount_list = pathname_list[-(required_dir_amount + 1):]
    return '/'.join(required_amount_list)
