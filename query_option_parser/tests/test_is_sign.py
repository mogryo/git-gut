"""Test is_sign"""

from query_option_parser.parser import is_sign


def test_correct_sign() -> None:
    """Test valid sign"""
    assert is_sign(">=")


def test_invalid_sign() -> None:
    """Test invalid sign"""
    assert not is_sign("w")
