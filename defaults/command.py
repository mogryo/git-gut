"""Defaults for command options"""
from enums.columns import CliTableColumn, SortingDirection

DEFAULT_COLUMNS = ",".join([
    CliTableColumn.FILE_NAME.value,
    CliTableColumn.LINE_COUNT.value,
    CliTableColumn.COMMIT_AMOUNT.value
])

DEFAULT_SORT = ",".join([
    f"{CliTableColumn.DELETED_ADDED_RATIO.value}-{SortingDirection.DESC.value}",
    f"{CliTableColumn.LINE_COUNT.value}-{SortingDirection.DESC.value}",
])
