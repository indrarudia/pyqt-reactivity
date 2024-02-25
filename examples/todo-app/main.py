import sys

from PyQt6.QtWidgets import QApplication

from Todo import todoRepository
from TodoList import TodoList
from TodoListViewModel import TodoListViewModel


def main() -> None:
    """
    The main function.
    """
    app = QApplication(sys.argv)

    todoListViewModel = TodoListViewModel(todoRepository)
    todoList = TodoList(todoListViewModel)

    todoList.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
