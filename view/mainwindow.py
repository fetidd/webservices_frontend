from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QLineEdit, QTableWidget, QHBoxLayout, QTableWidgetItem,
    QVBoxLayout, QWidget)
from lib.logger import createLogger
import lib.config as config

log = createLogger(__name__)


class WSMain(QMainWindow):
    """
    Main application window.
    """

    def __init__(self):
        log.debug("calling __init__")
        super().__init__()
        self._configure()
        self._addLogin()
        self._addTable()
        self._addButtons()
        log.debug("calling show")
        self.show()

    def toggleLogin(self, loggedIn):
        log.debug("toggleLogin called")
        inputs = [self.userInput, self.passInput]
        button = self.loginButton
        if loggedIn:
            for i in inputs:
                i.setDisabled(True)
            button.setText("Logout")
        else:
            for i in inputs:
                i.setDisabled(False)
            button.setText("Login")
            self.clearTable()
        log.debug("toggleLogin returning")

    def populateTable(self, transactions):
        """
        Fill the table with Transactions.
        """
        # clear current
        log.debug(f"populateTable called with {len(transactions)} transactions")
        row = 0
        table = self.table
        for transaction in sorted(transactions, reverse=True, key=lambda x: x["transactionstartedtimestamp"]):
            table.insertRow(row)
            col = 0
            # Build each row
            for field in config.tableHeaders:
                item = QTableWidgetItem(transaction.get(field, "-"))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                table.setItem(row, col, item)
                col += 1
            row += 1
        table.resizeColumnsToContents()
        log.debug("populateTable returning")

    def clearTable(self):
        self.table.setRowCount(0)
        log.debug("Table cleared!")

    # PRIVATE METHODS-------------------------------------------------------------------------------------------------
    def _configure(self):
        """Configure the main window geometry, layout and title."""
        log.debug("_configure called")
        self.setObjectName("MainWindow")
        self.setWindowTitle("Webservices Client")
        self.setFixedSize(1024, 768)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.layout = QVBoxLayout()
        centralWidget.setLayout(self.layout)
        log.debug("_configure returning")

    def _addLogin(self):
        """Create and add the login section to the main window."""
        log.debug("_addLogin called")
        layout = QHBoxLayout()
        userLabel = QLabel("Username")
        passLabel = QLabel("Password")
        userInput = QLineEdit()
        passInput = QLineEdit()
        # TODO remove this ------------------
        userInput.setText("ben_webservices")
        passInput.setText("BenPass123!")
        # -----------------------------------
        loginButton = QPushButton("Login")
        for w in [userLabel, userInput, passLabel, passInput, loginButton]:
            layout.addWidget(w)
        self.layout.addLayout(layout)
        self.userInput = userInput
        self.passInput = passInput
        self.loginButton = loginButton
        log.debug("_addLogin returning")

    def _addTable(self):
        """Create and add the transaction table to the main window."""
        log.debug("_addTable called")
        layout = QHBoxLayout()
        table = QTableWidget(0, len(config.tableHeaders))
        table.setHorizontalHeaderLabels(config.tableHeaders)
        table.resizeColumnsToContents()
        layout.addWidget(table)
        self.layout.addLayout(layout)
        self.table = table
        log.debug("_addTable returning")

    def _addButtons(self):
        """Create and add the button section to the main window."""
        log.debug("_addButtons called")
        layout = QHBoxLayout()
        buttons = ["transactionquery", "refund"]
        self.requestButtons = {}
        for b in buttons:
            btn = QPushButton(b.upper())
            self.requestButtons[b] = btn
            layout.addWidget(btn)
        self.layout.addLayout(layout)
        log.debug("_addButtons returning")
