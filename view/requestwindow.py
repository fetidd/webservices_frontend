from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QCalendarWidget, QHBoxLayout, QComboBox, QLineEdit, QPushButton, \
    QLabel, QWidget
from lib.logger import createLogger
from lib.requesttype import RequestType
from lib.config import FIELDS
log = createLogger(__name__)


# noinspection PyArgumentList
class RequestWindow(QDialog):
    def __init__(self, requestType: RequestType, transactions):
        super().__init__()
        log.debug("Creating a new RequestWindow")
        self.setWindowTitle(f"New {requestType.name}")
        self.requestType = requestType
        self.transactions = transactions
        self.layout = QVBoxLayout()
        self.rows = []
        if requestType == RequestType.TRANSACTIONQUERY:
            self._setupTransactionQuery()
        elif requestType == RequestType.REFUND:
            self._setupRefund()

    # PRIVATE METHODS ------------------------------------------------------------------------------------------------
    def _setupTransactionQuery(self):
        log.debug("Setting up TRANSACTIONQUERY window")
        instructions = """
        Select a start and end date for the period you wish to query.
        Click 'New field' to add a row containing a dropdown and input box to specify fields to filter with. 
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
        fields = [field for field, data in FIELDS.items() if data["inc"] & RequestType.TRANSACTIONQUERY.value]
        newFieldButton = QPushButton("New field", clicked=lambda: self._addDropdownRow(fields))
        self.submitButton = QPushButton("Submit request")
        row = QHBoxLayout()
        row.addWidget(newFieldButton)
        row.addWidget(self.submitButton)
        self.layout.addLayout(row)
        self.setLayout(self.layout)

    def _setupRefund(self):
        log.debug(f"Setting up REFUND window with {len(self.transactions)} transactions")
        if len(self.transactions) <= 1:
            self.requiredInputs = {}
            for field, data in FIELDS.items():
                if data["req"] & RequestType.REFUND.value:
                    row = QHBoxLayout()
                    fieldInput = QLineEdit()
                    self.requiredInputs[field] = fieldInput
                    row.addWidget(QLabel(field))
                    row.addWidget(fieldInput)
                    self.layout.addLayout(row)
            if len(self.transactions) == 1:
                transaction = self.transactions[0]
                self.requiredInputs["parenttransactionreference"].setText(transaction["transactionreference"])
                self.requiredInputs["sitereference"].setText(transaction["sitereference"])
            self.requiredInputs["requesttypedescriptions"].setText("REFUND")
            self.submitButton = QPushButton("Submit request")
            self.layout.addWidget(self.submitButton)
            self.setLayout(self.layout)
        else:  # open the batch window with a table of passed-in transactions
            pass

    def _setupTransactionUpdate(self):
        log.debug(f"Setting up TRANSACTIONUPDATE window with {len(self.transactions)} transactions")
        if len(self.transactions) <= 1:
            pass
        else:
            pass

    def _addDropdownRow(self, fields):
        rowCount = len(self.findChildren(QWidget, options=Qt.FindDirectChildrenOnly))
        row = QWidget(parent=self, objectName="requestRow")
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(2, 2, 2, 2)
        row.setLayout(layout)
        dropdown = QComboBox()
        dropdown.insertItem(0, "")
        for i, field in enumerate(fields):
            dropdown.insertItem(i, field)
        dropdownInput = QLineEdit()
        deleteButton = QPushButton("X", clicked=lambda: self._deleteRow(row))
        deleteButton.setFixedWidth(30)
        layout.addWidget(dropdown)
        layout.addWidget(dropdownInput)
        layout.addWidget(deleteButton)
        self.layout.insertWidget(rowCount-2, row)
        self.rows.append(row)
        log.debug(f"Added new row")

    def _deleteRow(self, row):
        self.layout.removeWidget(row)
        row.deleteLater()
        self.rows.remove(row)
        self.adjustSize()
        log.debug(f"Deleted row")
