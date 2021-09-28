from PySide6.QtGui import QBrush, QColor, Qt
from PySide6.QtWidgets import QTableWidgetItem


class TransactionTableItem(QTableWidgetItem):
    def __init__(self, text, ref):
        super().__init__(text)
        self.reference = ref

    def applyStatusColor(self, text):
        if text == "":
            self.setText("")
            return
        conversion = {
            "0": {"color": QBrush(Qt.cyan), "text": "Pending"},
            "1": {"color": QBrush(Qt.gray), "text": "Manual"},
            "10": {"color": QBrush(Qt.cyan), "text": "Settling"},
            "100": {"color": QBrush(Qt.green), "text": "Settled"},
            "2": {"color": QBrush(Qt.yellow), "text": "Suspended"},
            "3": {"color": QBrush(Qt.red), "text": "Cancelled"}
        }
        self.setBackground(conversion[text]["color"])
        self.setText(conversion[text]["text"])
