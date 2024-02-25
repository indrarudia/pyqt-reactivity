import copy
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSignal


@dataclass
class Todo:
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    isDone: bool = False
    createdAt: datetime = datetime.now()


class TodoRepository(QObject):
    modelChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.todos: list[Todo] = [
            Todo(
                name="Buy milk",
            ),
            Todo(
                name="Buy eggs",
            ),
            Todo(
                name="Buy bread",
            ),
        ]

    def notify(self) -> None:
        self.modelChanged.emit()

    def getAll(self) -> list[Todo]:
        return copy.deepcopy(sorted(self.todos, key=lambda todo: todo.createdAt))

    def getById(self, id: str) -> Todo:
        for todo in self.todos:
            if todo.id == id:
                return todo
        raise ValueError(f"Todo with id {id} not found.")

    def add(self, name: str, isDone: bool = False) -> None:
        todo = Todo(
            name=name,
            isDone=isDone,
        )
        self.todos.append(todo)
        self.notify()

    def update(self, id: str, name: str, isDone: bool) -> None:
        todo = self.getById(id)
        todo.name = name
        todo.isDone = isDone
        self.notify()

    def toggle(self, id: str) -> None:
        todo = self.getById(id)
        todo.isDone = not todo.isDone
        self.notify()

    def remove(self, id: str) -> None:
        todo = self.getById(id)
        self.todos.remove(todo)
        self.notify()

    def clear(self) -> None:
        self.todos = []
        self.notify()


todoRepository = TodoRepository()
