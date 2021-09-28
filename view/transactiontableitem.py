from PySide6.QtWidgets import QTableWidgetItem


class TransactionTableItem(QTableWidgetItem):
    def __init__(self, text, ref):
        super().__init__(text)
        self.reference = ref
