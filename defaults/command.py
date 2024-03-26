"""Defaults for command options"""
from enums.columns import CliTableColumn

DEFAULT_COLUMNS = ", ".join([
    CliTableColumn.ID.value,
    CliTableColumn.FILE_NAME.value,
    CliTableColumn.COMMIT_AMOUNT.value
])
