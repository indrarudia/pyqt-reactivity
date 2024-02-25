from PyQt6.QtCore import QItemSelection, Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListView,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)
from Todo import todoRepository
from TodoDetail import TodoDetail
from TodoDetailViewModel import TodoDetailViewModel
from TodoListViewModel import TodoListViewModel


class TodoList(QDialog):
    def __init__(self, viewModel: TodoListViewModel) -> None:
        super().__init__()

        self.viewModel = viewModel

        self.listTodo = QListView()
        self.model = QStandardItemModel(self.listTodo)
        self.model.itemChanged.connect(self.onItemChanged)
        self.listTodo.setModel(self.model)
        self.listTodo.selectionModel().selectionChanged.connect(self.onSelectionChanged)

        newButton = QPushButton("New")
        newButton.clicked.connect(self.openTodoDialog)

        editButton = QPushButton("Edit")
        editButton.clicked.connect(self.editTodo)
        editButton.setEnabled(self.viewModel.editButtonEnabled.value)
        self.viewModel.editButtonEnabled.watch(lambda it: editButton.setEnabled(it))

        deleteButton = QPushButton("Delete")
        deleteButton.clicked.connect(self.deleteTodo)
        deleteButton.setEnabled(self.viewModel.deleteButtonEnabled.value)
        self.viewModel.deleteButtonEnabled.watch(lambda it: deleteButton.setEnabled(it))

        spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        buttonLayout = QHBoxLayout()
        buttonLayout.addItem(spacer)
        buttonLayout.addWidget(newButton)
        buttonLayout.addWidget(editButton)
        buttonLayout.addWidget(deleteButton)

        listTodosLayout = QVBoxLayout()
        listTodosLayout.addLayout(buttonLayout)
        listTodosLayout.addWidget(self.listTodo)

        self.setLayout(listTodosLayout)
        self.setWindowTitle("Todo List")

        self.viewModel.uiState.watch(self.updateUi)
        self.updateUi()

    def updateUi(self) -> None:
        self.model.clear()
        for todo in self.viewModel.uiState.value.todoList:
            item = QStandardItem(todo.name)
            item.setCheckable(True)
            item.setCheckState(
                Qt.CheckState.Checked if todo.isDone else Qt.CheckState.Unchecked
            )
            self.model.appendRow(item)

    def onItemChanged(self, item: QStandardItem) -> None:
        # Unwatch to prevent infinite loop when the model is updated.
        self.viewModel.uiState.unwatch(self.updateUi)

        todo = self.viewModel.uiState.value.todoList[item.row()]
        self.viewModel.toggle(todo)

        # Re-watch the model.
        self.viewModel.uiState.watch(self.updateUi)

    def onSelectionChanged(self, selected: QItemSelection) -> None:
        if len(selected.indexes()) > 0:
            self.viewModel.selectedTodoIndex.value = selected.indexes()[0].row()
        else:
            self.viewModel.selectedTodoIndex.value = -1

    def openTodoDialog(self) -> None:
        viewModel = TodoDetailViewModel(todoRepository)
        dialog = TodoDetail(viewModel)
        dialog.exec()

    def editTodo(self) -> None:
        todo = self.viewModel.uiState.value.todoList[
            self.viewModel.selectedTodoIndex.value
        ]
        viewModel = TodoDetailViewModel(todoRepository, todo.id)
        dialog = TodoDetail(viewModel)
        dialog.exec()

    def deleteTodo(self) -> None:
        todo = self.viewModel.uiState.value.todoList[
            self.viewModel.selectedTodoIndex.value
        ]
        self.viewModel.delete(todo)
