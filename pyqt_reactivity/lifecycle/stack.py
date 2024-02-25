from typing import Callable, Generic, TypeVar, Union

T = TypeVar("T")


class Stack(Generic[T]):
    """
    A stack implementation supporting undo and redo operations.

    This stack allows pushing elements onto the stack or applying functions to
    the current element to generate new elements. It maintains an index to keep
    track of the current state for undo and redo operations.

    Attributes:
        stack (list): A list to store the elements in the stack.
        index (int): The current index indicating the active element in the stack.
        current (T): The current element at the top of the stack.
    """

    def __init__(self, current: T) -> None:
        self._stack: list[T] = [current]
        self._index: int = len(self.stack)
        self._current: T = current

    @property
    def stack(self) -> list[T]:
        return self._stack

    @property
    def index(self) -> int:
        return self._index

    @property
    def current(self) -> T:
        return self._current

    def update(self) -> T:
        self._current = self._stack[self._index - 1]
        return self._current

    def push(self, value: Union[T, Callable[[T], T]]) -> T:
        self._stack = self._stack[: self._index]
        if callable(value):
            self._stack.append(value(self._current))
        else:
            self._stack.append(value)
        self._index += 1
        return self.update()

    def undo(self) -> T:
        if self._index > 1:
            self._index -= 1
        return self.update()

    def redo(self) -> T:
        if self._index < len(self._stack):
            self._index += 1
        return self.update()

    def canUndo(self) -> bool:
        return self._index > 1
