from utils.filesystem import trim_directories


def test_long_path():
    assert trim_directories("../dir1/dir2/dir3/file", 2) == "dir2/dir3/file"


def test_short_path():
    assert trim_directories("/dir/file", 3) == "dir/file"


def test_empty_path():
    assert trim_directories("", 3) == ""
