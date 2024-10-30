"""Test are_column_name_valid"""

from enums.columns import CliTableColumn
from validators.statement_validators import are_column_names_valid


def test_valid_single_value() -> None:
    """Check valid single value in list"""
    assert are_column_names_valid([CliTableColumn.LINE_COUNT.value])


def test_valid_multiple_values() -> None:
    """Check multiple valid values in list"""
    assert are_column_names_valid(
        [
            CliTableColumn.LINE_COUNT.value,
            CliTableColumn.FILE_NAME.value,
            CliTableColumn.COMMIT_AMOUNT.value,
        ]
    )


def test_invalid_single_values() -> None:
    """Check single invalid values in list"""
    assert not are_column_names_valid(
        [
            "random name",
        ]
    )


def test_invalid_multiple_values() -> None:
    """Check multiple invalid values in list"""
    assert not are_column_names_valid(
        [
            "random name",
            "roger",
            "over",
        ]
    )


def test_empty_list() -> None:
    """Check empty list"""
    assert are_column_names_valid([])
