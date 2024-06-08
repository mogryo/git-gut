"""Builder pattern for column color"""

from typing import Self, List, Callable
from enums.columns import CliTableColumnColor


class ColorPipelineBuilder:
    """Builder for column color"""

    def __init__(self):
        self._pipe: List[Callable[[str], CliTableColumnColor]] = []

    def range(self, bottom: float, top: float, color: CliTableColumnColor) -> Self:
        """Set color for number range"""
        if top < bottom:
            raise ValueError("Value top cannot be less than bottom")

        self._pipe.append(lambda value: color if bottom <= float(value) < top else None)

        return self

    def from_value(self, bottom: float, color: CliTableColumnColor) -> Self:
        """Set color from value to infinity"""
        self._pipe.append(lambda value: color if bottom <= float(value) else None)

        return self

    def as_pipe(self) -> Callable[[str], str]:
        """Return a piped function, to match value to color"""
        pipe_functions = [*self._pipe]

        def call_pipe(value: str) -> str:
            """Returned function, to match color"""
            for func in pipe_functions:
                color = func(value)
                if color is not None:
                    return f"{color.value}{value}{CliTableColumnColor.RESET.value}"
            return value

        self._pipe = []
        return call_pipe
