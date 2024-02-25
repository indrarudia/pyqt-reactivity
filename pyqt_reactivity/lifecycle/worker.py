from typing import Any, Callable, Dict, Iterable, Optional, ParamSpec, TypeVar

from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal

T = TypeVar("T")
R = ParamSpec("R")


class Signal(QObject):
    started = pyqtSignal()
    resolved = pyqtSignal(object)
    rejected = pyqtSignal(Exception)
    finished = pyqtSignal()


class Worker(QRunnable):
    """
    A worker that move heavy function calculation to a thread.
    """

    def __init__(
        self,
        func: Callable[R, T],
        args: Optional[Iterable[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__()

        self.func = func
        self.signals = Signal()

        if args is not None:
            self.args = args
        else:
            self.args = ()

        if kwargs is not None:
            self.kwargs = kwargs
        else:
            self.kwargs = {}

    def run(self) -> None:
        self.signals.started.emit()
        try:
            result = self.func(*self.args, **self.kwargs)
            self.signals.resolved.emit(result)
        except Exception as e:
            self.signals.rejected.emit(e)
        finally:
            self.signals.finished.emit()


def noop(*args: Any, **kwargs: Dict[Any, Any]) -> None:
    """A function that does nothing."""
    pass


class Dispatcher(QObject):
    """
    A dispatcher that launch a function in a thread.
    """

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.threadpool = QThreadPool(self)

    def launch(
        self,
        func: Callable[R, T],
        args: Optional[Iterable[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        onSuccess: Callable[[T], None] = noop,
        onError: Callable[[Exception], None] = noop,
        onStarted: Callable[..., None] = noop,
        onFinished: Callable[..., None] = noop,
    ) -> None:
        t = Worker(func, args=args, kwargs=kwargs)
        t.setAutoDelete(True)
        t.signals.started.connect(onStarted)
        t.signals.resolved.connect(onSuccess)
        t.signals.rejected.connect(onError)
        t.signals.finished.connect(onFinished)

        self.threadpool.start(t)

    def cancel(self) -> None:
        self.threadpool.waitForDone()
