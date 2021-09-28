from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QLineEdit, QHBoxLayout,
    QVBoxLayout, QWidget)
from lib.logger import createLogger
from view.transactiontable import TransactionTable

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
            self.table.clear()
        log.debug("toggleLogin returning")

    # PRIVATE METHODS-------------------------------------------------------------------------------------------------
    def _configure(self):
        """Configure the main window geometry, layout and title."""
        log.debug("_configure called")
        self.setObjectName("MainWindow")
        self.setWindowTitle("Webservices Client")
        self.resize(1400, 1000)
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
        self.userInput = QLineEdit()
        self.passInput = QLineEdit()
        # TODO remove this ------------------
        self.userInput.setText("ben_webservices")
        self.passInput.setText("BenPass123!")
        # -----------------------------------
        self.loginButton = QPushButton("Login")
        for w in [userLabel, self.userInput, passLabel, self.passInput, self.loginButton]:
            layout.addWidget(w)
        self.layout.addLayout(layout)
        log.debug("_addLogin returning")

    def _addTable(self):
        """Create and add the transaction table to the main window."""
        log.debug("_addTable called")
        layout = QHBoxLayout()
        table = TransactionTable()
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
