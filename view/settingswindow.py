from PySide6.QtWidgets import QDialog, QGroupBox, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton
from lib.logger import createLogger

log = createLogger(__name__)


class SettingsWindow(QDialog):
    def __init__(self, currentConfig):
        super().__init__()
        self.config = currentConfig
        self.setWindowTitle("Edit Settings")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # setup window
        self.selectedHeaders = {
            field: data for field, data in self.config.FIELDS.items() if data["isActive"]
        }
        self.unselectedHeaders = {
            field: data for field, data in self.config.FIELDS.items() if not data["isActive"]
        }
        self._tableHeaderSettings()
        self._addButtons()

    def _tableHeaderSettings(self):
        box = QGroupBox("Table Headers")
        mainLayout = QHBoxLayout()
        box.setLayout(mainLayout)
        left, middle, right = QVBoxLayout(), QVBoxLayout(), QVBoxLayout()
        self.layout.addWidget(box)
        for layout in left, middle, right:
            mainLayout.addLayout(layout)
        # Left
        self.selectedHeaderList = QListWidget()
        left.addWidget(self.selectedHeaderList)
        # Middle
        self.left = QPushButton("<--")
        self.right = QPushButton("-->")
        self.up, self.down = QPushButton("Move up"), QPushButton("Move down")
        for btn in self.left, self.right, self.up, self.down:
            middle.addWidget(btn)
        # Right
        self.unselectedHeaderList = QListWidget()
        right.addWidget(self.unselectedHeaderList)
        self.refreshHeaderSettings()

    def refreshHeaderSettings(self):
        self.selectedHeaderList.clear()
        self.unselectedHeaderList.clear()
        self.selectedHeaders = {
            field: data for field, data in self.config.FIELDS.items() if data["isActive"]
        }
        self.unselectedHeaders = {
            field: data for field, data in self.config.FIELDS.items() if not data["isActive"]
        }
        for header, _ in sorted(self.selectedHeaders.items(), key=lambda x: x[1]["position"]):
            self.selectedHeaderList.addItem(header)
        for header in self.unselectedHeaders.keys():
            self.unselectedHeaderList.addItem(header)

    def _addButtons(self):
        layout = QHBoxLayout()
        self.layout.addLayout(layout)
        self.saveButton, self.defaultButton, self.applyButton = \
            QPushButton("Save"), QPushButton("Default"), QPushButton("Apply")
        for btn in self.saveButton, self.defaultButton, self.applyButton:
            layout.addWidget(btn)
