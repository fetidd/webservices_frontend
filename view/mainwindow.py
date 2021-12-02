from PySide6.QtGui import QAction
from lib.requesttype import RequestType
from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QLineEdit, QHBoxLayout,
    QVBoxLayout, QWidget, QMenuBar, QMenu)
from lib.logger import createLogger
from view.transactiontable import TransactionTable
from dotenv import load_dotenv
import os

load_dotenv()
log = createLogger(__name__)


class WSMain(QMainWindow):
    """
    Main application window.
    """

    def __init__(self, config):
        log.debug("calling __init__")
        super().__init__()
        self._config = config
        self._configure()
        self._addMenubar()
        self._addLogin()
        self._addTable()
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

    def _configure(self):
        """Configure the main window geometry, layout and title."""
        log.debug("_configure called")
        self.setObjectName("MainWindow")
        self.setWindowTitle("Webservices Client")
        self.resize(900, 700)
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
        self.userInput.setText(os.environ.get("WS_USERNAME", ""))
        self.passInput = QLineEdit()
        self.passInput.setEchoMode(QLineEdit.Password)
        self.passInput.setText(os.environ.get("WS_PASSWORD", ""))
        self.loginButton = QPushButton("Login")
        for w in [userLabel, self.userInput, passLabel, self.passInput, self.loginButton]:
            layout.addWidget(w)
        self.layout.addLayout(layout)
        log.debug("_addLogin returning")

    def _addTable(self):
        """Create and add the transaction table to the main window."""
        log.debug("_addTable called")
        layout = QHBoxLayout()
        table = TransactionTable(self._config)
        layout.addWidget(table)
        self.layout.addLayout(layout)
        self.table = table
        log.debug("_addTable returning")

    def _addMenubar(self):
        bar = QMenuBar()
        # Create menus
        requestMenu = QMenu("&New Request")
        settingsMenu = QMenu("&Settings")
        # Create and add actions
        self.requestActions = {rt.name: QAction(f"&{rt.name}") for rt in list(RequestType) if rt.name not in ["NONE", "TRANSACTIONUPDATE"]}
        self.settingsAction = QAction("&Edit")
        for action in self.requestActions.values():
            requestMenu.addAction(action)
        settingsMenu.addAction(self.settingsAction)
        # Add menus to menubar
        bar.addMenu(requestMenu)
        bar.addMenu(settingsMenu)
        # Set the menubar for the window
        self.setMenuBar(bar)
