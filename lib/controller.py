import copy
import os.path
import pickle

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QComboBox

from lib.config import Config
from lib.logger import createLogger
from view.errordialog import Error
from view.infowindow import Info
from view.mainwindow import WSMain
from view.responsewindow import ResponseWindow
from view.requestwindow import RequestWindow
from lib.requesttype import RequestType
from view.settingswindow import SettingsWindow

log = createLogger(__name__)


def analyseResponses(responses: list) -> dict:
    """Expects a list of the inner responses from the outer gateway response."""
    log.debug(f"Analysing {responses}")
    analysis = {
        res.get("referenceForResult", "NOREF!"): {"response": res, "error": not not int(res.get("errorcode", "ERROR!"))}
        for res in responses}
    log.debug(f"\t->> {len(analysis.keys())}: {analysis}")
    return analysis


class Controller:
    def __init__(self, view, model, api, config):
        self.view: WSMain = view
        self.model = model
        self.api = api
        self.config = config
        self.selectedTransactions = []
        self.requestWindow = None
        self.configCopy = None
        self._connectMainWindowComponents()

    def _connectMainWindowComponents(self):
        log.debug("_connectMainWindowComponents called")
        # Login Section
        self.view.loginButton.clicked.connect(self._login)
        # Table Section
        self.view.table.itemSelectionChanged.connect(self._selectTransactions)
        self.view.table.itemDoubleClicked.connect(self._showTransactionInfo)

        # Actions menu
        def connectRequestAction(action):  # Function required due to lazy lambda?
            requestType = RequestType[action.text().lstrip('&')]
            action.triggered.connect(lambda: self._openRequestWindow(requestType))

        for a in self.view.requestActions.values():
            connectRequestAction(a)
        log.debug("_connectMainWindowComponents returning")
        # Settings menu
        self.view.settingsAction.triggered.connect(self._openSettingsWindow)

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
                self.view.table.populate(self.model.getAll())
            self.view.toggleLogin(self.api.loggedIn)
        log.debug("_login returning")
        return

    # REQUESTS --------------------------------------------------------------------------------------------------------
    def _openRequestWindow(self, requestType):
        log.debug(f"_openRequestWindow({requestType.name}) called")
        if not self.api.loggedIn:
            Error("Not logged in!").exec()
            return
        if self.requestWindow is not None:  # This should never happen 
            raise Exception("There is already a request window open!")
        try:
            self.requestWindow = RequestWindow(requestType, self.selectedTransactions)
        except Exception as e:
            log.error(e)
            Error(e).exec()
            return
        self.requestWindow.submitButton.clicked.connect(self._submitRequest)
        self.requestWindow.exec()
        self.requestWindow = None
        log.debug("_openRequestWindow returning")

    def _submitRequest(self):
        log.debug("_submitRequest called")
        window = self.requestWindow
        if window.requestType == RequestType.TRANSACTIONQUERY:
            self._submitTRANSACTIONQUERY(window)
        elif window.requestType == RequestType.REFUND:
            self._submitREFUND(window)
        elif window.requestType == RequestType.CUSTOM:
            self._submitCUSTOM(window)
        elif window.requestType == RequestType.AUTH:
            self._submitAUTH(window)
        elif window.requestType == RequestType.ACCOUNTCHECK:
            self._submitACCOUNTCHECK(window)
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
            self.view.table.clear()
            self.view.table.populate(self.model.getAll())
            window.close()
        else:
            msg = "Didn't find any transactions for supplied filter"
            log.error(msg)
            Error(msg).exec()
        log.debug("_submitTRANSACTIONQUERY returning")

    def _submitREFUND(self, window):
        responses = []
        if len(window.transactions) > 0:
            for t in window.transactions:
                if t["requesttypedescription"] == "AUTH" and t["settlestatus"] == "100":
                    gatewayResponse = self.api.makeRequest({
                        "parenttransactionreference": t["transactionreference"],
                        "requesttypedescriptions": ["REFUND"],
                        "sitereference": t["sitereference"]
                    })
                    response = gatewayResponse["responses"][0]
                    response["referenceForResult"] = t["transactionreference"]
                    responses += (gatewayResponse["responses"])
        else:
            # gather data from the window to submit
            response = self.api.makeRequest({
                "parenttransactionreference": window.requiredInputs["parenttransactionreference"].text(),
                "requesttypedescriptions": ["REFUND"],
                "sitereference": window.requiredInputs["sitereference"].text()
            })
            response["referenceForResult"] = window.requiredInputs["parenttransactionreference"].text()
            responses.append(response)
        ResponseWindow(analyseResponses(responses)).exec()

    def _submitCUSTOM(self, window):
        # Build a request object from the inputted data
        request = {}
        rows = [{row.findChild(QComboBox): row.findChild(QLineEdit)} for row in window.rows]
        for row in rows:
            if list(row.keys())[0].currentText() == "requesttypedescriptions":
                # create the requesttypedescriptions list from comma separated input
                request["requesttypedescriptions"] = [reqType.strip() for reqType in
                                                      list(row.values())[0].text().split(',')]
            else:
                request[list(row.keys())[0].currentText()] = list(row.values())[0].text()
        # Remove empty rows from the filter
        if "" in request.keys():
            del request[""]
        # make the request
        gatewayResponse = self.api.makeRequest(request)
        responses = []
        for response in gatewayResponse["responses"]:
            response["referenceForResult"] = response.get("transactionreference", "ERROR!")
            responses.append(response)
        ResponseWindow(analyseResponses(responses)).exec()

    def _submitAUTH(self, window):
        request = {f: v.text() for f, v in window.requiredInputs.items()}
        request["requesttypedescriptions"] = ["AUTH"]
        # get customs rows
        rows = [{row.findChild(QComboBox): row.findChild(QLineEdit)} for row in window.rows]
        for row in rows:
            request[list(row.keys())[0].currentText()] = list(row.values())[0].text()
        # Remove empty rows from the filter
        if "" in request.keys():
            del request[""]
        # make the request
        gatewayResponse = self.api.makeRequest(request)
        responses = []
        for response in gatewayResponse["responses"]:
            response["referenceForResult"] = response.get("transactionreference", "ERROR!")
            responses.append(response)
        ResponseWindow(analyseResponses(responses)).exec()

    def _submitACCOUNTCHECK(self, window):
        """Accountcheck to tokenise payment details on gateway"""
        request = {f: v.text() for f, v in window.requiredInputs.items()}
        request["requesttypedescriptions"] = ["ACCOUNTCHECK"]
        request["credentialsonfile"] = "1"
        # get customs rows
        rows = [{row.findChild(QComboBox): row.findChild(QLineEdit)} for row in window.rows]
        for row in rows:
            request[list(row.keys())[0].currentText()] = list(row.values())[0].text()
        # Remove empty rows from the filter
        if "" in request.keys():
            del request[""]
        # make the request
        gatewayResponse = self.api.makeRequest(request)
        responses = []
        for response in gatewayResponse["responses"]:
            response["referenceForResult"] = response.get("transactionreference", "ERROR!")
            responses.append(response)
        ResponseWindow(analyseResponses(responses)).exec()

    def _selectTransactions(self):
        log.debug("selecting transactions")
        table = self.view.table
        self.selectedTransactions = []
        for selectedRange in table.selectedRanges():
            for transaction in table.transactions[selectedRange.topRow():selectedRange.bottomRow() + 1]:
                self.selectedTransactions.append(transaction)

    def _showTransactionInfo(self, transaction):
        Info(self.model.get(transaction.reference)).exec()

    # SETTINGS WINDOW ------------------------------------------------------------------------------------------------
    def _openSettingsWindow(self):
        log.debug("_openSettingsWindow called")
        self.configCopy = copy.deepcopy(self.config)
        window = SettingsWindow(self.configCopy)
        # connect save and default buttons
        window.applyButton.clicked.connect(lambda: self._applySettings())
        window.saveButton.clicked.connect(lambda: self._saveSettings())
        window.defaultButton.clicked.connect(lambda: self._returnToDefaultSettings(window))
        # connect left and right arrows
        window.left.clicked.connect(lambda: self._toggleHeaderState(window, True))
        window.right.clicked.connect(lambda: self._toggleHeaderState(window, False))
        window.up.clicked.connect(lambda: self._moveHeader(window, "up"))
        window.down.clicked.connect(lambda: self._moveHeader(window, "down"))

        window.exec()

    def _saveSettings(self):
        pickle.dump(self.config, open("./settings.pkl", "wb"))

    def _applySettings(self):
        self.config.FIELDS = self.configCopy.FIELDS
        self.view.table.clear()
        self.view.table.setupTableHeaders()
        self.view.table.populate(self.model.getAll())

    def _returnToDefaultSettings(self, window):
        fields = Config().FIELDS
        self.config.FIELDS = fields
        self.configCopy.FIELDS = fields
        if os.path.exists("./settings.pkl"):
            os.remove("./settings.pkl")
        self.view.table.clear()
        self.view.table.setupTableHeaders()
        self.view.table.populate(self.model.getAll())
        window.refreshHeaderSettings()

    def _toggleHeaderState(self, window: SettingsWindow, state: bool):
        log.debug(f"_toggleHeaderState({state}) called")
        headers = window.unselectedHeaderList.selectedItems() if state else window.selectedHeaderList.selectedItems()
        for header in headers:
            field = self.configCopy.FIELDS[header.text()]
            field["isActive"] = state
            field["position"] = window.selectedHeaderList.count() if state else None
            log.debug(f"{field['humanString']} is {state} at position {field['position']}")
        window.refreshHeaderSettings()

    def _moveHeader(self, window: SettingsWindow, direction: str):
        log.debug(f"_moveHeader({direction}) called")
        headers = window.selectedHeaderList.selectedItems()
        for header in headers:
            field = self.configCopy.FIELDS[header.text()]
            origPos = field["position"]
            newPos = None
            if direction == "up":
                if origPos == 0:
                    log.debug(f"\t{header.text()} is at the top already...")
                    return
                newPos = origPos - 1
            elif direction == "down":
                if origPos == window.selectedHeaderList.count()-1:
                    log.debug(f"\t{header.text()} is at the bottom already...")
                    return
                newPos = origPos + 1
            else:
                raise Exception("Argument was neither up nor down!")
            for swapped, data in self.configCopy.FIELDS.items():
                if data["position"] == newPos:
                    data["position"] = origPos
                    log.debug(f"\t{swapped} was at {newPos}, moved to {origPos}")
                    break
            field["position"] = newPos
            log.debug(f"\t{header.text()} was at {origPos}, moved to {newPos}")
            window.refreshHeaderSettings()
