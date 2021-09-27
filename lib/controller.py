from PySide6.QtWidgets import QLineEdit, QPushButton
from lib.logger import createLogger
from view.errordialog import Error
from view.requestwindow import RequestWindow
from lib.requesttype import RequestType

log = createLogger(__name__)


class Controller:
    def __init__(self, view, model, api):
        self.view = view
        self.model = model
        self.api = api
        self.selectedTransactions = []
        self._connectMainWindowComponents()

    def _connectMainWindowComponents(self):
        log.debug("_connectMainWindowComponents called")
        # Login Section
        self.view.loginButton.clicked.connect(self._login)

        # Table Section

        # Buttons Section
        def connectRequestButton(button):  # Function required due to lazy lambda?
            requestType = RequestType[button.text().upper()]
            button.clicked.connect(lambda: self._openRequestWindow(requestType))
        for btn in self.view.requestButtons.values():
            connectRequestButton(btn)
        log.debug("_connectMainWindowComponents returning")

    def _login(self):
        log.debug("_login called")
        # If logged in, log out
        if self.api.loggedIn:
            self.api.st = None
            self.api.loggedIn = False
            self.view.toggleLogin(self.api.loggedIn)
        else:
            # get username and password from main window
            username = self.view.userInput.text()
            password = self.view.passInput.text()
            # try to log in
            try:
                response = self.api.login(username, password)
            except Exception as e:
                log.error(e)
                Error(e).exec()
                log.debug("_login returning")
                return
            # populate table if transactions are found
            if int(response["responses"][0]["found"]) > 0:
                log.debug(f"Populating  table with {response['responses'][0]['found']} transactions")
                self.model.add(response["responses"][0]["records"])
                self.view.populateTable(self.model.getAll())
            self.view.toggleLogin(self.api.loggedIn)
        log.debug("_login returning")
        return

    def _openRequestWindow(self, requestType):
        log.debug(f"_openRequestWindow({requestType.name}) called")
        window = RequestWindow(requestType, self.selectedTransactions)
        window.submitButton.clicked.connect(lambda: self._submitRequest(requestType, window.transactions))
        window.exec()
        log.debug("_openRequestWindow returning")

    def _submitRequest(self, requestType, transactions):
        pass
