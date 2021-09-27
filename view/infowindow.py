from PySide6.QtWidgets import QMessageBox


class Info(QMessageBox):
    def __init__(self, transaction: dict):
        super().__init__()
        self.info = transaction
        self.setWindowTitle(self.info["transactionreference"])
        self.setText(str(self.info))
