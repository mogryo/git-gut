"""Test trim_directories."""

from utils.filesystem import trim_directories


def test_long_path():
    """Test long path - function should shorten the path."""
    assert trim_directories("../dir1/dir2/dir3/file", 2) == "dir2/dir3/file"


def test_short_path():
    """Test short path - initial string should not be changed"""
    assert trim_directories("/dir/file", 3) == "dir/file"


def test_empty_path():
    """Provide empty string, nothing should be changed."""
    assert trim_directories("", 3) == ""
