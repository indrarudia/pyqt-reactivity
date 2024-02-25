from dataclasses import dataclass, field

from Todo import Todo, TodoRepository

from pyqt_reactivity import Ref, computed, ref
from pyqt_reactivity.lifecycle import ViewModel


@dataclass(frozen=True)
class UiState:
    todoList: list[Todo] = field(default_factory=list)


class TodoListViewModel(ViewModel):
    def __init__(self, todoRepository: TodoRepository) -> None:
        super().__init__()

        self._todoRepository = todoRepository
        self._uiState: Ref[UiState] = ref(
            UiState(todoList=self._todoRepository.getAll())
        )

        self.selectedTodoIndex: Ref[int] = ref(-1)

        def editButtonEnabled(selectedTodoIndex: Ref[int]) -> bool:
            return selectedTodoIndex.value != -1

        self.editButtonEnabled = computed(
            editButtonEnabled, args=(self.selectedTodoIndex,)
        )

        def deleteButtonEnabled(selectedTodoIndex: Ref[int]) -> bool:
            return selectedTodoIndex.value != -1

        self.deleteButtonEnabled = computed(
            deleteButtonEnabled, args=(self.selectedTodoIndex,)
        )

        self._todoRepository.modelChanged.connect(self.onModelChanged)

    @property
    def uiState(self) -> Ref[UiState]:
        return self._uiState

    @property
    def todoRepository(self) -> TodoRepository:
        return self._todoRepository

    def onModelChanged(self) -> None:
        self.uiState.value = UiState(todoList=self.todoRepository.getAll())

    def delete(self, todo: Todo) -> None:
        self.todoRepository.remove(todo.id)

    def toggle(self, todo: Todo) -> None:
        self.todoRepository.toggle(todo.id)
