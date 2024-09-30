"""Enums for user input"""

from enum import StrEnum


class QueryKeywords(StrEnum):
    """Query keywords"""

    SHOW = "SHOW"
    FROM = "FROM"
    WHERE = "WHERE"
    ORDERBY = "ORDERBY"
    SINCE = "SINCE"
    UNTIL = "UNTIL"
