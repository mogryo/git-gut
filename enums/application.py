"""Global applicaiton enums"""

from enum import Enum


class Severity(Enum):
    """Severity level enum"""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    INFO = "INFO"
    WARNING = "WARNING"


class TableLibrary(Enum):
    """Options for CLI table library"""

    PRETTY_TABLE = "pretty"
    RICH_TABLE = "rich"
