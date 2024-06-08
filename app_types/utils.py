"""Types and enums for utils."""

from typing import TypedDict, Optional


class GenerateUniqueKeysKwargs(TypedDict):
    """Kwargs for generating unique keys"""

    start_key: int
    end_key: int
    key_length: Optional[int]


class ColumnBuilderKwargs(TypedDict):
    """Kwargs for ColumnBuilder"""

    pathname_length: Optional[int]
