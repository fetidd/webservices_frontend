from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableView, QTableWidgetItem
from lib.config import tableHeaders
from lib.logger import createLogger
from view.transactiontableitem import TransactionTableItem

log = createLogger(__name__)


class TransactionTable(QTableWidget):
    def __init__(self):
        super().__init__(0, len(tableHeaders))
        self.setHorizontalHeaderLabels(tableHeaders)
        self.resizeColumnsToContents()
        self.setSelectionBehavior(QTableView.SelectRows)
        self.transactions = []

    def populate(self, transactions):
        """
        Fill the table with Transactions.
        """
        # clear current
        log.debug(f"populateTable called with {len(transactions)} transactions")
        row = 0
        for transaction in sorted(transactions, reverse=True, key=lambda x: x["transactionstartedtimestamp"]):
            self.insertRow(row)
            col = 0
            # Build each row
            for field in tableHeaders:
                item = TransactionTableItem(text=transaction.get(field, "-"), ref=transaction["transactionreference"])
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                self.setItem(row, col, item)
                col += 1
            row += 1
            self.transactions.append(transaction)
        self.resizeColumnsToContents()
        log.debug("populateTable returning")

    def clear(self):
        self.setRowCount(0)
        self.transactions = []
        log.debug("Table cleared!")
