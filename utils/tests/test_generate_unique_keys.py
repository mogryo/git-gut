"""Test generate_unique_keys"""
from utils.id_generator import generate_unique_keys


def test_length_of_list() -> None:
    """Check list is of correct length"""
    result = generate_unique_keys(start_key=0, end_key=3)
    assert len(result) == 4


def test_start_key_is_first_element() -> None:
    """Check first element in sequence is as specified"""
    result = generate_unique_keys(start_key=3, end_key=9, key_length=1)
    assert result[0] == "3"


def test_end_key_is_last_element() -> None:
    """Check last element in sequence is as specified"""
    result = generate_unique_keys(start_key=0, end_key=9, key_length=1)
    assert result[-1] == "9"
