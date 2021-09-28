from PySide6.QtWidgets import QMessageBox


class Info(QMessageBox):
    def __init__(self, transaction: dict):
        super().__init__()
        self.transaction = transaction
        self.setWindowTitle(self.transaction["transactionreference"])
        self.setText(self.buildString())

    def buildString(self) -> str:
        string = ""
        for k, v in self.transaction.items():
            string += f"{k}: {v}\n"
        return string

