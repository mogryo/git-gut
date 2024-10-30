"""Result dataclass"""

from typing import Generic, TypeVar, Callable, List, Any

T = TypeVar("T")
E = TypeVar("E")
V = TypeVar("V")


class ResultOk(Generic[T]):
    """Successful result"""

    def __init__(self, value: T):
        """Constructor"""
        self._value: T = value

    def map(self, func: Callable[[T], T]):
        """Map value to new value of same type"""
        return ResultOk(func(self._value))

    @property
    def value(self):
        """Value property"""
        return self._value


class ResultValidationError(Generic[V]):
    """Validation result"""

    def __init__(self, value: Any, validation_err: List[V]):
        """Constructor"""
        self._value = value
        self._validation_error: List[V] = validation_err

    @property
    def value(self):
        """Value property"""
        return self._value

    @property
    def validation_error(self) -> List[V]:
        """List of validation error"""
        return self._validation_error


class ResultException(Generic[E]):
    """Exception result"""

    def __init__(self, value: Any, error: E):
        """Constructor"""
        self._value = value
        self._error = error

    @property
    def value(self):
        """Value property"""
        return self._value

    @property
    def error(self) -> E:
        """Exception property"""
        return self._error


type ResultUnion[T, V, E] = ResultOk[T] | ResultValidationError[V] | ResultException[E]
