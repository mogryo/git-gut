"""Test stringify_unique_key"""
import pytest
from utils.id_generator import stringify_unique_key


def test_short_number() -> None:
    """Test zeros are prefixed correctly"""
    result = stringify_unique_key(10, 5)
    assert result == "00010"


def test_longer_number() -> None:
    """Test too long number throws exception"""
    with pytest.raises(ValueError):
        stringify_unique_key(100, 2)


def test_max_length() -> None:
    """Test allowed length number is parsed"""
    result = stringify_unique_key(100, 3)
    assert result == "100"
