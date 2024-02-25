from threading import Lock
from typing import Callable, TypeVar

from .base import T, hasChanged
from .ref import Ref

U = TypeVar("U")


class BindingRef(Ref[T]):
    def __init__(
        self, ref: Ref[U], getter: Callable[[U], T], setter: Callable[[U, T], T]
    ):
        initialValue = getter(ref.value)
        super().__init__(initialValue)

        self._ref = ref
        self._getter = getter
        self._setter = setter
        self._lock = Lock()

        self._preventSubscribeOnUpdate = False

        ref.watch(lambda it: self._subscribe(it))

    def _subscribe(self, newValue: T) -> None:
        if self._preventSubscribeOnUpdate:
            self._preventSubscribeOnUpdate = False
            return

        with self._lock:
            if hasChanged(self._value, self.get()):
                self._value = self.get()
                self.notify()

    def get(self) -> T:
        return self._getter(self._ref.value)

    def set(self, newValue: T) -> None:
        self._preventSubscribeOnUpdate = True

        def updateRefState(state: U) -> U:
            return self._setter(state, newValue)

        self._ref.update(updateRefState)

        with self._lock:
            if hasChanged(self._value, newValue):
                self._value = newValue
                self.notify()

    def __repr__(self) -> str:
        return f"<BindingRef: {self.get()}>"


def bind(ref: Ref[U], getter: Callable[[U], T], setter: Callable[[U, T], T]):
    return BindingRef(ref, getter, setter)


def bindProperty(ref: Ref[U], key: str, setter: Callable[[U, T], T]) -> BindingRef[T]:
    getter = lambda it: getattr(it, key)
    return bind(ref, getter, setter)


def observeProperty(ref: Ref[U], key: str) -> BindingRef[T]:
    getter = lambda it: getattr(it, key)

    def setter(it: U, value: T) -> U:
        raise RuntimeError("observeProperty is readonly.")

    return bind(ref, getter, setter)
