"""Utilities to mutate, query GitStat orm"""
from typing import List, Any
from sqlalchemy import select, Select, asc, desc
from enums.columns import CliTableColumn, SortingDirection
from orm.git_stat import GitStat
from app_types.dataclasses import SortingRule


def prepare_all_rows(column_names: List[CliTableColumn], rows: List[List[Any]]) -> List[GitStat]:
    """Prepare rows into GitStat ORM"""
    if len(column_names) == 0:
        return []

    git_stats = []
    for row in rows:
        data_for_git_stat = {}
        for index, column_name in enumerate(column_names):
            data_for_git_stat[column_name.value] = row[index]
        git_stats.append(
            GitStat(**data_for_git_stat)
        )

    return git_stats


COLUMN_TO_GIT_STAT_MAPPING = {
    column.value: getattr(GitStat, column.value) for column in CliTableColumn
}


def prepare_select(column_names: List[CliTableColumn]) -> Select:
    """Prepare select statement for specified columns"""
    git_stat_columns = []
    for column_name in column_names:
        git_stat_columns.append(COLUMN_TO_GIT_STAT_MAPPING[column_name.value])

    return select(*git_stat_columns)


def prepare_order_by(sorting_rules: List[SortingRule], select_statement: Select) -> Select:
    """Add sorting to select statement"""
    order_by_list = []
    for rule in sorting_rules:
        order_direction = asc if rule.sort_direction == SortingDirection.ASC else desc
        order_by_list.append(order_direction(COLUMN_TO_GIT_STAT_MAPPING[rule.column_name.value]))

    return select_statement.order_by(*order_by_list)
