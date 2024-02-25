from typing import Callable

from .ref import Ref
from .base import T


def isRef(value: T) -> bool:
    """Check if value is a reactive object."""
    if hasattr(value, "_isRef"):
        return True
    return False


def unref(ref: T | Ref) -> T:
    if isRef(ref):
        return ref.value
    return ref


def isComputedRef(value: T) -> bool:
    """Check if value is computed ref object."""
    if hasattr(value, "_isRef") and hasattr(value, "_isComputedRef"):
        return True
    return False


def toValue(value: T | Ref | Callable[..., T]) -> T:
    """Convert value to its value."""
    if isRef(value):
        return value.value
    if callable(value):
        return value()
    return value
