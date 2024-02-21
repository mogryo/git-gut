from typing import List
import re


def filter_out_directories(all_files: List[str], exclude_list: List[str]) -> List[str]:
    if (exclude_paths := "|".join(exclude_list)) != "":
        return list(filter(lambda x: not re.search(exclude_paths, x), all_files))

    return [*all_files]


def trim_directories(path: str, required_dir_amount: int) -> str:
    pathname_list = list(filter(lambda split_path: len(split_path) > 0, path.split("/")))
    required_amount_list = pathname_list[-(required_dir_amount + 1):]
    return '/'.join(required_amount_list)
