from typing import List
from git import Tree, Git
from app_types.utils import FileCommitStats


def get_flat_file_tree(tree: Tree) -> List[str]:
    generated_list = []
    for entry in tree:
        if entry.type == "blob":
            generated_list.append(entry.path)
        if entry.type == "tree":
            generated_list.extend(get_flat_file_tree(entry))

    return generated_list


def get_file_stats(git_instance: Git, filepath: str) -> List[FileCommitStats]:
    raw_result: str = git_instance.log('--follow', '--numstat', '--pretty=tformat:', '--', filepath)
    commit_list = raw_result.splitlines()

    result = []
    for commit_stat in commit_list:
        split_stat = commit_stat.split()
        result.append(FileCommitStats(split_stat[0], split_stat[1]))

    return result
