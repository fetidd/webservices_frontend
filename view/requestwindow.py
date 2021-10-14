from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QCalendarWidget, QHBoxLayout, QComboBox, QLineEdit, QPushButton, \
    QLabel, QWidget, QTableWidget, QTableWidgetItem, QTableView
from lib.logger import createLogger
from lib.requesttype import RequestType
from lib.config import Config

log = createLogger(__name__)

cfg = Config()


# noinspection PyArgumentList
class RequestWindow(QDialog):
    def __init__(self, requestType: RequestType, transactions):
        super().__init__()
        log.debug("Creating a new RequestWindow")
        self.setWindowTitle(f"New {requestType.name}")
        self.requestType = requestType
        self.transactions = transactions
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.rows = []
        if requestType == RequestType.TRANSACTIONQUERY:
            self._setupTransactionQuery()
        elif requestType == RequestType.REFUND:
            try:
                self._setupRefund()
            except Exception:
                raise
        elif requestType == RequestType.CUSTOM:
            self._setupCustom()
        elif requestType == RequestType.AUTH:
            self._setupAuth()
        elif requestType == RequestType.ACCOUNTCHECK:
            self._setupAccountCheck()
        else:
            raise Exception("This request is not written yet.")

    # PRIVATE METHODS ------------------------------------------------------------------------------------------------
    def _setupTransactionQuery(self):
        log.debug("Setting up TRANSACTIONQUERY window")
        instructions = """
        Select a start and end date for the period you wish to query.
        Click 'New field' to add a row containing a dropdown and input box to specify cfg.FIELDS to filter by. 
        To add multiple values for the same filter, separate the values with commas.
        """
        self.layout.addWidget(QLabel(instructions))
        # Add start and end date picker row
        row = QWidget()
        rowLayout = QHBoxLayout()
        row.setLayout(rowLayout)
        self.startInput = QCalendarWidget()
        self.endInput = QCalendarWidget()
        rowLayout.addWidget(self.startInput)
        rowLayout.addWidget(self.endInput)
        self.layout.addWidget(row)
        # Add new field and submit buttons
        fields = [field for field, data in cfg.FIELDS.items() if data["inc"] & RequestType.TRANSACTIONQUERY.value]
        newFieldButton = QPushButton("New field", clicked=lambda: self._addDropdownRow(fields))
        newFieldButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.submitButton = QPushButton("Submit request")
        self.submitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        row = QHBoxLayout()
        row.addWidget(newFieldButton)
        row.addWidget(self.submitButton)
        self.layout.addLayout(row)

    def _setupRefund(self):
        log.debug(f"Setting up REFUND window with {len(self.transactions)} transactions")
        if len(self.transactions) == 0:
            instructions = """
            Enter the details of the transaction you wish to refund.
            Only AUTHS that have settled (settlestatus=100) can be refunded.
            """
            self.layout.addWidget(QLabel(instructions))
            self.requiredInputs = {}
            for field, data in cfg.FIELDS.items():
                if data["req"] & RequestType.REFUND.value:
                    row = QHBoxLayout()
                    fieldInput = QLineEdit()
                    self.requiredInputs[field] = fieldInput
                    row.addWidget(QLabel(field))
                    row.addWidget(fieldInput)
                    self.layout.addLayout(row)
            self.requiredInputs["requesttypedescriptions"].setText("REFUND")
            self.submitButton = QPushButton("Submit request")
            self.layout.addWidget(self.submitButton)
        else:  # open the batch window with a table of passed-in transactions
            instructions = """
            Make sure the transactions in the table are the ones you wish to refund.
            Only AUTHS that have settled (settlestatus=100) can be refunded.
            """
            self.layout.addWidget(QLabel(instructions))
            # Remove transactions that are not AUTHS with settlestatus=100
            transactions = [t for t in self.transactions if
                            t["requesttypedescription"] == "AUTH" and t["settlestatus"] == "100"]
            # Show a table with the remaining transactions, doubleclickable and selectable
            self.resize(600, 400)
            self.table = QTableWidget(0, 3)
            self.table.setSelectionBehavior(QTableView.SelectRows)
            self.table.setHorizontalHeaderLabels(["parenttransactionreference", "baseamount", "customername"])
            for index, transaction in enumerate(transactions):
                self.table.insertRow(index)
                ref = QTableWidgetItem(transaction["transactionreference"])
                amount = QTableWidgetItem(transaction["baseamount"])
                customerName = QTableWidgetItem(
                    f"{transaction.get('billingfirstname', '')} {transaction.get('billinglastname', '')}")
                for i, w in enumerate([ref, amount, customerName]):
                    w.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                    self.table.setItem(index, i, w)
            self.table.resizeColumnsToContents()
            self.layout.addWidget(self.table)
            self.submitButton = QPushButton("Submit request")
            self.submitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.layout.addWidget(self.submitButton)

    def _setupCustom(self):
        log.debug("Setting up CUSTOM window")
        instructions = """
        Click 'New field' to add a row containing a dropdown and input box to enter a value for the field.
        When submitting you must ensure the cfg.FIELDS and values follow the specification for the requesttype as shown 
        in the docs. 
        To add multiple values for the same field, separate the values with commas.
        """
        self.layout.addWidget(QLabel(instructions))
        # Add new field and submit buttons
        fields = [field for field, data in cfg.FIELDS.items() if data["inc"] & RequestType.CUSTOM.value]
        newFieldButton = QPushButton("New field", clicked=lambda: self._addDropdownRow(fields))
        newFieldButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.submitButton = QPushButton("Submit request")
        self.submitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        row = QHBoxLayout()
        row.addWidget(newFieldButton)
        row.addWidget(self.submitButton)
        self.layout.addLayout(row)
        # Add some initial empty rows as there won't be any at all when this window opens
        for i in range(6):
            self._addDropdownRow(fields)

    def _setupAuth(self):
        log.debug("Setting up AUTH window")
        instructions = """"""
        self.layout.addWidget(QLabel(instructions))
        self.requiredInputs = {}
        for field, data in cfg.FIELDS.items():
            if data["req"] & RequestType.AUTH.value:
                row = QHBoxLayout()
                fieldInput = QLineEdit()
                self.requiredInputs[field] = fieldInput
                row.addWidget(QLabel(field))
                row.addWidget(fieldInput)
                self.layout.addLayout(row)
        self.requiredInputs["requesttypedescriptions"].setText("AUTH")
        # Add new field and submit buttons
        fields = [field for field, data in cfg.FIELDS.items() if data["inc"] & RequestType.AUTH.value]
        newFieldButton = QPushButton("New field", clicked=lambda: self._addDropdownRow(fields))
        newFieldButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.submitButton = QPushButton("Submit request")
        self.submitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        row = QHBoxLayout()
        row.addWidget(newFieldButton)
        row.addWidget(self.submitButton)
        self.layout.addLayout(row)

    def _setupAccountCheck(self):
        log.debug("Setting up ACCOUNTCHECK window")
        instructions = """"""
        self.layout.addWidget(QLabel(instructions))
        self.requiredInputs = {}
        for field, data in cfg.FIELDS.items():
            if data["req"] & RequestType.ACCOUNTCHECK.value or data["req"] & RequestType.AUTH.value:
                row = QHBoxLayout()
                fieldInput = QLineEdit()
                self.requiredInputs[field] = fieldInput
                row.addWidget(QLabel(field))
                row.addWidget(fieldInput)
                self.layout.addLayout(row)
        self.requiredInputs["requesttypedescriptions"].setText("ACCOUNTCHECK")
        # Add new field and submit buttons
        fields = [field for field, data in cfg.FIELDS.items() if data["inc"] & RequestType.ACCOUNTCHECK.value]
        newFieldButton = QPushButton("New field", clicked=lambda: self._addDropdownRow(fields))
        newFieldButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.submitButton = QPushButton("Submit request")
        self.submitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        row = QHBoxLayout()
        row.addWidget(newFieldButton)
        row.addWidget(self.submitButton)
        self.layout.addLayout(row)

    def _addDropdownRow(self, fields):
        rowCount = len(self.findChildren(QWidget, options=Qt.FindDirectChildrenOnly))
        row = QWidget(parent=self, objectName="requestRow")
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(2, 2, 2, 2)
        row.setLayout(layout)
        dropdown = QComboBox()
        dropdown.insertItem(0, "")
        for i, field in enumerate(sorted(fields)):
            dropdown.insertItem(i + 1, field)
        dropdownInput = QLineEdit()
        deleteButton = QPushButton("X", clicked=lambda: self._deleteRow(row))
        deleteButton.setFixedWidth(30)
        deleteButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(dropdown)
        layout.addWidget(dropdownInput)
        layout.addWidget(deleteButton)
        self.layout.addWidget(row)
        self.rows.append(row)
        log.debug(f"Added new row")

    def _deleteRow(self, row):
        self.layout.removeWidget(row)
        row.deleteLater()
        self.rows.remove(row)
        self.adjustSize()
        log.debug(f"Deleted row")




