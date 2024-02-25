from typing import Generic, TypeVar

from ..ref import Ref
from .stack import Stack

T = TypeVar("T")


class UndoStack(Generic[T]):
    """
    A stack implementation supporting undo and redo operations for reactive
    state.
    """

    def __init__(self, state: Ref[T]) -> None:
        self._stack = Stack(state.value)
        self._preventSubscribeOnUpdate = False
        self._state = state

        state.watch(lambda it: self._subscribe(it))

    def _subscribe(self, newState: T) -> None:
        if self._preventSubscribeOnUpdate:
            self._preventSubscribeOnUpdate = False
            return
        self._stack.push(newState)

    def undo(self) -> None:
        self._preventSubscribeOnUpdate = True
        self._state.value = self._stack.undo()

    def redo(self) -> None:
        self._preventSubscribeOnUpdate = True
        self._state.value = self._stack.redo()

    def canUndo(self) -> bool:
        return self._stack.canUndo()
