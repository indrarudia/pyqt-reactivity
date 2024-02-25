from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)
from TodoDetailViewModel import TodoDetailViewModel


class TodoDetail(QDialog):
    def __init__(self, viewModel: TodoDetailViewModel) -> None:
        super().__init__()

        self.viewModel = viewModel

        nameLineEdit = QLineEdit()
        nameLineEdit.setText(self.viewModel.uiState.value.name)
        nameLineEdit.textChanged.connect(self.viewModel.setName)

        isDoneCheckBox = QCheckBox()
        isDoneCheckBox.setChecked(self.viewModel.uiState.value.isDone)
        isDoneCheckBox.stateChanged.connect(self.viewModel.setIsDone)

        contentLayout = QFormLayout()
        contentLayout.addRow("Name", nameLineEdit)
        contentLayout.addRow("Is Done", isDoneCheckBox)

        saveButton = QPushButton("Save")
        saveButton.setEnabled(self.viewModel.isSaveEnabled.value)
        self.viewModel.isSaveEnabled.watch(lambda it: saveButton.setEnabled(it))
        saveButton.clicked.connect(self.save)

        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)

        horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        buttonLayout = QHBoxLayout()
        buttonLayout.addItem(horizontalSpacer)
        buttonLayout.addWidget(saveButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(contentLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

        self.setWindowTitle("Todo Detail")

    def save(self) -> None:
        self.viewModel.save()
        self.close()
