from typing import Any, Callable, ParamSpec, TypeVar, Generic

from PyQt6.QtCore import QObject, pyqtSignal

T = TypeVar("T")
R = ParamSpec("R")


class BaseRef(QObject, Generic[T]):
    _isRef = True

    valueChanged = pyqtSignal(object)

    def notify(self) -> None:
        self.valueChanged.emit(self.get())

    @property
    def value(self) -> T:
        return self.get()

    @value.setter
    def value(self, newValue: T) -> None:
        self.set(newValue)

    def __str__(self) -> str:
        return str(self.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def watch(self, func: Callable[R, None]) -> None:
        self.valueChanged.connect(func)

    def unwatch(self, func: Callable[R, None]) -> None:
        self.valueChanged.disconnect(func)

    def get(self) -> T:
        raise NotImplementedError

    def set(self, newValue: T) -> None:
        raise NotImplementedError


def hasChanged(value: Any, oldValue: Any) -> bool:
    """Check if value is equal to oldValue."""
    return value != oldValue
