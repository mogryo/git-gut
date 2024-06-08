"""Test split_sign_condition_string"""

from query_option_parser.parser import split_sign_condition_string


def test_valid_condition_string() -> None:
    """Test valid condition string"""
    result = split_sign_condition_string("linecount > 100")
    assert result[0] == "linecount"
    assert result[1] == ">"
    assert result[2] == "100"


def test_invalid_condition_string() -> None:
    """Test invalid condition string"""
    result = split_sign_condition_string("linecount haha 100")
    assert result[0] == "linecounthaha"
    assert result[1] != "haha"
    assert result[2] != "100"
