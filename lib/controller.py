from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QPushButton, QComboBox
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
        self.requestWindow = None
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
                Error(e).exec()
                log.debug("_login returning")
                return
            # populate table if transactions are found
            if int(response["found"]) > 0:
                log.debug(f"Populating table with {len(response['found'])} transactions")
                self.model.add(response["records"])
                self.view.populateTable(self.model.getAll())
            self.view.toggleLogin(self.api.loggedIn)
        log.debug("_login returning")
        return

    def _openRequestWindow(self, requestType):
        log.debug(f"_openRequestWindow({requestType.name}) called")
        if not self.api.loggedIn:
            Error("Not logged in!").exec()
            return
        if self.requestWindow is not None:
            raise Exception("There is already a request window open!")
        self.requestWindow = RequestWindow(requestType, self.selectedTransactions)
        self.requestWindow.submitButton.clicked.connect(self._submitRequest)
        self.requestWindow.exec()
        self.requestWindow = None
        log.debug("_openRequestWindow returning")

    def _submitRequest(self):
        log.debug("_submitRequest called")
        window = self.requestWindow
        if window.requestType == RequestType.TRANSACTIONQUERY:
            self._submitTRANSACTIONQUERY(window)
        log.debug("_submitRequest returning")

    def _submitTRANSACTIONQUERY(self, window):
        log.debug("_submitTRANSACTIONQUERY called")
        # Get selected start and end dates
        start = window.startInput.selectedDate().toString(Qt.DateFormat.ISODate) + " 00:00:00"
        end = window.endInput.selectedDate().toString(Qt.DateFormat.ISODate) + " 23:59:59"
        # Create a filter from the dropdown rows
        rows = [{row.findChild(QComboBox): row.findChild(QLineEdit)} for row in window.rows]
        reqFilter = {list(row.keys())[0].currentText(): [{"value": val.strip()} for val in
                                                         list(row.values())[0].text().split(',')] for row in rows}
        # Remove empty rows from the filter
        if "" in reqFilter.keys():
            del reqFilter[""]
        reqFilter["starttimestamp"] = [{"value": start}]
        reqFilter["endtimestamp"] = [{"value": end}]
        response = self.api.makeRequest({
            "requesttypedescriptions": ["TRANSACTIONQUERY"],
            "filter": reqFilter
        })
        response = response["responses"][0]
        if response["errorcode"] != "0":
            errString = f"{response['errorcode']} {response['errormessage']} {response['errordata']}"
            Error(errString).exec()
            log.error(errString)
        elif int(response["found"]) > 0:
            self.model.clear()
            self.model.add(response["records"])
            self.view.clearTable()
            self.view.populateTable(self.model.getAll())
            window.close()
        else:
            msg = "Didn't find any transactions for supplied filter"
            log.error(msg)
            Error(msg).exec()
        log.debug("_submitTRANSACTIONQUERY returning")

