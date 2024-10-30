"""Git repo validators"""

import sys
from git import Repo
from app_types.result import ResultUnion, ResultException


def assert_repo_result_is_valid(repo_result: ResultUnion[Repo]):
    """Validate repo instance result"""
    match repo_result:
        case ResultException():
            print("Provided FROM path is not GIT repository")
            sys.exit()
