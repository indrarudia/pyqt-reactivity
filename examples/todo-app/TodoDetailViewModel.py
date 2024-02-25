from dataclasses import dataclass, field, replace

from Todo import TodoRepository

from pyqt_reactivity import Ref, computed, ref
from pyqt_reactivity.lifecycle import ViewModel


@dataclass(frozen=True)
class UiState:
    name: str = ""
    isDone: bool = False


class TodoDetailViewModel(ViewModel):
    def __init__(
        self, todoRepository: TodoRepository, todoId: str | None = None
    ) -> None:
        super().__init__()

        self._todoRepository = todoRepository
        self._todoId = todoId
        if self._todoId is not None:
            todo = self._todoRepository.getById(self._todoId)
            state = UiState(name=todo.name, isDone=todo.isDone)
        else:
            state = UiState()
        self._uiState: Ref[UiState] = ref(state)

        def isSaveEnabled(uiState: Ref[UiState]) -> bool:
            return uiState.value.name != ""

        self._isSaveEnabled = computed(isSaveEnabled, args=(self._uiState,))

    @property
    def uiState(self) -> Ref[UiState]:
        return self._uiState

    @property
    def todoRepository(self) -> TodoRepository:
        return self._todoRepository

    @property
    def isSaveEnabled(self) -> Ref[bool]:
        return self._isSaveEnabled

    def setName(self, name: str) -> None:
        self.uiState.update(lambda it: replace(it, name=name))

    def setIsDone(self, isDone: bool) -> None:
        self.uiState.update(lambda it: replace(it, isDone=bool(isDone)))

    def save(self) -> None:
        if self._todoId is not None:
            self.todoRepository.update(
                id=self._todoId,
                name=self.uiState.value.name,
                isDone=self.uiState.value.isDone,
            )
        else:
            self.todoRepository.add(
                name=self.uiState.value.name,
                isDone=self.uiState.value.isDone,
            )
