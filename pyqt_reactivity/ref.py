from collections.abc import Callable
from threading import Lock

from .base import BaseRef, R, T, hasChanged


class Ref(BaseRef[T]):
    def __init__(self, value: T) -> None:
        super().__init__()

        self._value = value
        self._lock = Lock()

    def get(self) -> T:
        return self._value

    def set(self, newValue: T) -> None:
        with self._lock:
            if hasChanged(self._value, newValue):
                self._value = newValue
                self.notify()

    def update(self, func: Callable[R, T]) -> None:
        newValue = func(self._value)
        self.set(newValue)

    def __repr__(self) -> str:
        return f"<Ref: {self.get()}>"


class ReadonlyRef(Ref[T]):
    def set(self, newValue: T) -> None:
        raise RuntimeError("Ref is readonly")


def ref(value: T) -> Ref[T]:
    return Ref[T](value)
