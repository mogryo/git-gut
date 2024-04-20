"""Test is_number"""
from utils.numbers import is_number


def test_valid_float_number() -> None:
    """Test float number"""
    assert is_number("3.01")


def test_valid_negative_number() -> None:
    """Test negative number"""
    assert is_number("-3")


def test_invalid_string() -> None:
    """Test random characters do not pass"""
    assert not is_number("asd")
