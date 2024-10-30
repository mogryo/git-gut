"""Node/statement validation errors"""

from dataclasses import dataclass

from enums.application import Severity


@dataclass
class NodeValidationError:
    """Node validation error"""

    statement_part: str
    message: str
    severity: Severity
