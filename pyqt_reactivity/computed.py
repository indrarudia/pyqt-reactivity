from collections.abc import Callable
from typing import Any, Dict, Iterable

from .base import BaseRef, T, R
from .ref import Ref
from .utils import isRef


class ComputedRef(BaseRef[T]):
    _isComputedRef = True

    def __init__(
        self,
        getter: Callable[R, T],
        args: Iterable[Ref] | None = None,
        kwargs: Dict[str, Ref] | None = None,
    ) -> None:
        super().__init__()

        self.getter = getter
        if args is not None:
            self.args = args
        else:
            self.args = list()
        if kwargs is not None:
            self.kwargs = kwargs
        else:
            self.kwargs = dict()

        for arg in self.args:
            if isRef(arg):
                arg.valueChanged.connect(self.notify)

        for kw in self.kwargs.values():
            if isRef(kw):
                kw.valueChanged.connect(self.notify)

    def get(self) -> Callable[R, T]:
        return self.getter(*self.args, **self.kwargs)

    def set(self, newValue: Any) -> None:
        raise RuntimeError("ComputedRef is readonly")

    def __repr__(self) -> str:
        return f"<ComputedRef: {self.get()}>"


def computed(
    getter: Callable[R, T],
    args: Iterable[Ref] | None = None,
    kwargs: Dict[str, Ref] | None = None,
) -> ComputedRef[T]:
    return ComputedRef[T](getter, args, kwargs)
