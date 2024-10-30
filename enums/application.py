"""Global applicaiton enums"""

from enum import Enum


class Severity(Enum):
    """Severity level enum"""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    INFO = "INFO"
    WARNING = "WARNING"
