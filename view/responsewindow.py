from PySide6.QtWidgets import QMessageBox

# TODO improve this
class ResponseWindow(QMessageBox):
    def __init__(self, response):
        super().__init__()
        self.response = response
        self.setWindowTitle("Received response...")
        self.setText(self.buildString())

    def buildString(self) -> str:
        string = ""
        for k, v in self.response.items():
            string += f"{k}: {v}\n"
        return string
