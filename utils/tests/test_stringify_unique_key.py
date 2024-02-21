from utils.id_generator import stringify_unique_key
import pytest


def test_short_number() -> None:
    result = stringify_unique_key(10, 5)
    assert result == "00010"


def test_longer_number() -> None:
    with pytest.raises(ValueError):
        stringify_unique_key(100, 2)


def test_max_length() -> None:
    result = stringify_unique_key(100, 3)
    assert result == "100"
