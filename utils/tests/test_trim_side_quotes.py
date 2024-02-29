"""Test trim side quotes"""
from utils.text import trim_side_quotes


def test_empty_string():
    """Test empty string - result should be empty string as well"""
    assert trim_side_quotes("") == ""


def test_text_with_no_quotes():
    """Test text which does not contain double quotes - result initial string"""
    assert trim_side_quotes("Hey") == "Hey"


def test_text_with_quotes_at_sides():
    """Double quotes at start and end should be removed"""
    assert trim_side_quotes("\"Howdy\"") == "Howdy"


def test_start_double_quotes():
    """If double quote only at the beginning - nothing should be removed"""
    assert trim_side_quotes("\"A") == "\"A"


def test_end_double_quotes():
    """If double quote only at the end - nothing should be removed"""
    assert trim_side_quotes("A\"") == "A\""
