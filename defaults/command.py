"""Defaults for command options"""
from enums.columns import CliTableColumn, SortingDirection, CliTableColumnColor

DEFAULT_COLUMNS = ",".join([
    CliTableColumn.FILE_NAME.value,
    CliTableColumn.LINE_COUNT.value,
    CliTableColumn.COMMIT_AMOUNT.value
])

DEFAULT_SORT = ",".join([
    f"{CliTableColumn.DELETED_ADDED_RATIO.value}-{SortingDirection.DESC.value}",
    f"{CliTableColumn.LINE_COUNT.value}-{SortingDirection.DESC.value}",
])

DEFAULT_COLORS = ";".join([
    f"{CliTableColumn.DELETED_ADDED_RATIO.value}"
    f"-0,0.15,{CliTableColumnColor.GREEN.name}"
    f"/0.15,0.3,{CliTableColumnColor.YELLOW.name}"
    f"/0.3,,{CliTableColumnColor.RED.name};",
    f"{CliTableColumn.LINE_COUNT.value}"
    f"-0,250,{CliTableColumnColor.GREEN.name}"
    f"/250,400,{CliTableColumnColor.YELLOW.name}"
    f"/400,,{CliTableColumnColor.RED.name};"
])
