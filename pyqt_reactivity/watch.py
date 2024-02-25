from collections.abc import Callable

from .base import R
from .computed import ComputedRef
from .ref import Ref


def watch(ref: Ref | ComputedRef, callback: Callable[R, None]) -> None:
    ref.watch(callback)


def unwatch(ref: Ref | ComputedRef, callback: Callable[R, None]) -> None:
    ref.unwatch(callback)
