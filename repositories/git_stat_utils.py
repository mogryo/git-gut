"""Utilities to mutate, query GitStat orm"""
from typing import List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, Result
from enums.columns import CliTableColumn
from orm.git_stat import GitStat


def add_all_rows(column_names: List[CliTableColumn], rows: List[List[Any]], session: Session) -> None:
    """Add all git stat rows to table"""
    git_stats = []
    for row in rows:
        data_for_git_stat = {}
        for index, column_name in enumerate(column_names):
            data_for_git_stat[column_name.value] = row[index]
        git_stats.append(
            GitStat(**data_for_git_stat)
        )

    session.add_all(git_stats)
    session.commit()


# Todo: Automate this dictionary creation
mapping = {
    CliTableColumn.ID.value: GitStat.id,
    CliTableColumn.FILE_NAME.value: GitStat.filename,
    CliTableColumn.LINE_COUNT.value: GitStat.linecount,
    CliTableColumn.COMMIT_AMOUNT.value: GitStat.commitcount,
    CliTableColumn.DELETED_ADDED_RATIO.value: GitStat.daratio,
    CliTableColumn.MOST_ADDED_AUTHOR.value: GitStat.maauthor,
    CliTableColumn.MOST_DELETED_AUTHOR.value: GitStat.mdauthor,
    CliTableColumn.MOST_FREQUENT_AUTHOR.value: GitStat.mfauthor,
}


def read_all_rows(column_names: List[CliTableColumn], session: Session) -> Result[Any]:
    """Read all required columns from table"""
    git_stat_columns = []
    for column_name in column_names:
        git_stat_columns.append(mapping[column_name.value])

    statement = select(*git_stat_columns)
    return session.execute(statement)
