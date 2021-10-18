from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableView
from lib.config import Config
from lib.logger import createLogger
from view.transactiontableitem import TransactionTableItem

log = createLogger(__name__)


class TransactionTable(QTableWidget):
    def __init__(self, config):
        super().__init__(0, 0)
        self.config = config
        self.transactions = []
        self.setupTableHeaders()
        self.resizeColumnsToContents()
        self.setSelectionBehavior(QTableView.SelectRows)

    def setupTableHeaders(self):
        activeFields = {field: data for field, data in self.config.FIELDS.items() if data["isActive"]}
        # Sort the headers
        headers = [data["humanString"] for field, data in sorted(activeFields.items(), key=lambda f: f[1]["position"])]
        # Apply the headers
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

    def populate(self, transactions):
        """
        Fill the table with Transactions.
        """
        log.debug(f"populateTable called with {len(transactions)} transactions")
        row = 0
        for transaction in sorted(transactions, reverse=True, key=lambda x: x["transactionstartedtimestamp"]):
            self.insertRow(row)
            col = 0
            # Build each row
            activeFields = {field: data for field, data in self.config.FIELDS.items() if data["isActive"]}
            for field, data in sorted(activeFields.items(), key=lambda x: x[1]["position"]):
                if data["isActive"]:
                    text = transaction.get(field, "")
                    if field == "baseamount":
                        text = f"{float(text)/100:.2f} {transaction.get('currencyiso3a', '')}"
                    item = TransactionTableItem(text=text, ref=transaction["transactionreference"])
                    if field == "settlestatus":
                        item.applyStatusColor(text)
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
