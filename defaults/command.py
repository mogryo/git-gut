"""Defaults for command options"""

from enums.table import CliTableColumn, SortingDirection

DEFAULT_COLUMNS = ",".join(
    [
        CliTableColumn.FILE_NAME.value,
        CliTableColumn.LINE_COUNT.value,
        CliTableColumn.COMMIT_AMOUNT.value,
    ]
)

DEFAULT_SORT = ",".join(
    [
        f"{CliTableColumn.DELETED_ADDED_RATIO.value}-{SortingDirection.DESC.value}",
        f"{CliTableColumn.LINE_COUNT.value}-{SortingDirection.DESC.value}",
    ]
)

DEFAULT_COLORS = [
    (
        CliTableColumn.LINE_COUNT,
        {"green": (0, 250), "yellow": (250, 400), "red": (400,)},
    ),
    (
        CliTableColumn.DELETED_ADDED_RATIO,
        {"green": (0, 0.5), "yellow": (0.5, 0.9), "red": (0.9,)},
    ),
]
