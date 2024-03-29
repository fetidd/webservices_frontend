from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableView
from lib.config import Config
from lib.logger import createLogger
from view.transactiontableitem import TransactionTableItem

log = createLogger(__name__)
cfg = Config()


class TransactionTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 0)
        self._setupTableHeaders()
        self.setSelectionBehavior(QTableView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.transactions = []

    def _setupTableHeaders(self):
        headers = [(d["humanString"], d["position"]) for h, d in cfg.FIELDS.items() if d["activeInTransactionTableHeader"]]
        # Sort the headers
        headers = [header for header, position in sorted(headers, key=lambda h: h[1])]
        # Apply the headers
        self.setColumnCount(len(headers))
        self.verticalHeader().setVisible(False)
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
            for field, data in sorted(cfg.FIELDS.items(), key=lambda i: i[1]["position"]):
                if data["activeInTransactionTableHeader"]:
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
        log.debug("populateTable returning")

    def clear(self):
        self.setRowCount(0)
        self.transactions = []
        log.debug("Table cleared!")
