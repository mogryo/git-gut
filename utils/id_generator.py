"""Functions to generate unique keys."""

from typing import List, Unpack
from app_types.utils import GenerateUniqueKeysKwargs


def stringify_unique_key(number: int, key_length: int = 5) -> str:
    """
    Turns integer into string, but adds zeros at the beginning of string.
    :param number: Number itself.
    :param key_length: Length of desired keys (how many zeros added in front).
    :return:
    """
    string_number = str(number)
    prefix_length = key_length - len(string_number)

    if len(string_number) > key_length:
        raise ValueError(
            "Argument number must have less or equal digits to value key_length"
        )

    return ("0" * prefix_length) + string_number


def generate_unique_keys(**kwargs: Unpack[GenerateUniqueKeysKwargs]) -> List[str]:
    """
    Generate unique number keys as list of string.
    :param kwargs: GenerateUniqueKeysKwargs
    :return: List of generated keys.
    """
    start_key = kwargs.get("start_key", 0)
    end_key = kwargs.get("end_key", 100)
    key_length = kwargs.get("key_length", 5)

    return [
        stringify_unique_key(number, key_length)
        for number in range(start_key, end_key + 1)
    ]
