from PySide6.QtWidgets import QMessageBox


class Error(QMessageBox):
    def __init__(self, error):
        super().__init__()
        self.error = error
        self.setWindowTitle("Error")
        self.setText(str(error))