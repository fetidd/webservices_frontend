from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class ResponseWindow(QDialog):
    def __init__(self, responses: dict):
        super().__init__()
        self.responses = responses
        self.setWindowTitle("Received response...")
        self.setFixedWidth(400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        for ref, res in self.responses.items():
            self.layout.addWidget(self._createResponseWidget(ref, res))
        # todo: format each response into a widget (successgful and failed version, maybe the failed ones can have retry functionality?)
        # make them all selectable?
        # add each response widget to a layout in the window

    def _createResponseWidget(self, ref, response):
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(QLabel(ref))
        if not response["error"]:
            widget.setStyleSheet("background-color:green; color:white;")
        else:
            widget.setStyleSheet("background-color:red; color:white;")
        layout.addWidget(QLabel(response["response"].get("errormessage", "Success")))
        layout.addWidget(QLabel(str(response["response"].get("errordata", ""))))
        return widget
