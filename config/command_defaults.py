"""Defaults for command options"""
from app_types import CliTableColumn


DEFAULT_COLUMNS = ", ".join([
    CliTableColumn.ID.value,
    CliTableColumn.FILE_NAME.value,
    CliTableColumn.COMMIT_AMOUNT.value
])