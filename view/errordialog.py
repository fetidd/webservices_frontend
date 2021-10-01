from PySide6.QtWidgets import QMessageBox
from lib.logger import createLogger

log = createLogger(__name__)


class Error(QMessageBox):
    def __init__(self, error):
        super().__init__()
        self.error = error
        self.setWindowTitle("Error")
        self.setText(str(error))
        log.debug(f"Error dialog created [{error}]")
