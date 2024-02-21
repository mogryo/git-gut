"""Test filter_out_directories"""
from utils.filesystem import filter_out_directories


def test_empty_file_list() -> None:
    """Provide empty file list."""
    assert not filter_out_directories([], ['non-empty'])


def test_empty_exclude_list() -> None:
    """Provide empty list for exclude_list parameter."""
    input_array = ['/home/dir1', '/home/dir2']
    result = filter_out_directories(input_array, [])
    assert len(input_array) == len(result) and all(a == b for a, b in zip(input_array, result))


def test_exclude_directories() -> None:
    """Provide valid file list and exclude list."""
    result = filter_out_directories(['/home/dir1', '/work/dir2', '/work/dir3'], ['work/'])
    assert len(result) == 1 and result[0] == '/home/dir1'
