"""Utils for file names and directories"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
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
    pathname_list = list(
        filter(lambda split_path: len(split_path) > 0, path.split("/"))
    )
    required_amount_list = pathname_list[-(required_dir_amount + 1) :]
    return "/".join(required_amount_list)


def is_macos() -> bool:
    """Check if filesystem is macos"""
    return sys.platform == "darwin"


def is_linux() -> bool:
    """Check if filesystem is linux"""
    return sys.platform == "linux"


def get_stored_queries_file_path() -> Tuple[str, str]:
    """Get file path of file which contains saved queries"""
    if is_macos() or is_linux():
        return (
            os.path.join(os.path.expanduser("~"), ".git-gut"),
            "stored-queries.json",
        )

    return os.path.dirname(os.path.abspath(__file__)), "stored-queries.json"


def get_stored_queries_from_file() -> Dict[str, str]:
    """Get all stored queries"""
    file_path = get_stored_queries_file_path()
    try:
        with open(
            os.path.join(file_path[0], file_path[1]), "r", encoding="utf-8"
        ) as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_queries_to_file(queries: Dict[str, str]) -> None:
    """Saves queries to file"""
    file_path = get_stored_queries_file_path()
    Path.mkdir(Path(file_path[0]), exist_ok=True, parents=True)
    with open(os.path.join(file_path[0], file_path[1]), "w", encoding="utf-8") as file:
        # noinspection PyTypeChecker
        json.dump(queries, file)
