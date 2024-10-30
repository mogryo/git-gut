"""Result dataclass"""

from typing import Generic, TypeVar, Callable, List, Any

T = TypeVar("T")
E = TypeVar("E")
V = TypeVar("V")


class ResultOk(Generic[T]):
    def __init__(self, value: T):
        self._value: T = value

    def map(self, func: Callable[[T], T]):
        return ResultOk(func(self._value))

    @property
    def value(self):
        return self._value


class ResultValidationError(Generic[V]):
    def __init__(self, value: Any, validation_err: List[V]):
        self._value = value
        self._validation_error: List[V] = validation_err

    @property
    def value(self):
        return self._value

    @property
    def validation_error(self) -> List[V]:
        return self._validation_error


class ResultException(Generic[E]):
    def __init__(self, value: Any, error: E):
        self._value = value
        self._error = error

    @property
    def value(self):
        return self._value

    @property
    def error(self) -> E:
        return self._error


type ResultUnion[T, V, E] = ResultOk[T] | ResultValidationError[V] | ResultException[E]
