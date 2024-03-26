"""Types and enums for utils."""
from typing import TypedDict, Optional
from dataclasses import dataclass


class GenerateUniqueKeysKwargs(TypedDict):
    """Kwargs for generating unique keys"""
    start_key: int
    end_key: int
    key_length: Optional[int]


@dataclass
class FileCommitStats:
    """Dataclass for file commit stats information"""
    added_lines: int
    removed_lines: int
    author: str


class ColumnBuilderKwargs(TypedDict):
    """Kwargs for ColumnBuilder"""
    pathname_length: Optional[int]
