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
        # Add start and end date picker row
        self.startInput = QCalendarWidget()
        self.endInput = QCalendarWidget()
        self.layout.addWidget(self.startInput)
        self.layout.addWidget(self.endInput)
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
            self.requiredInputs["resquesttypedescriptions"].setText("REFUND")
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
        row = QWidget(parent=self, objectName="requestRow")
        layout = QHBoxLayout()
        row.setLayout(layout)
        self.rows.append(row)
        dropdown = QComboBox()
        dropdown.insertItem(0, "Choose one...")
        for i, field in enumerate(fields):
            dropdown.insertItem(i, field)
        dropdownInput = QLineEdit()
        dropdownInput.setObjectName(f"{self.requestType.name}.input.{self.rows.index(row)}")
        self.layout.insertWidget(2, row)
        layout.addWidget(dropdown)
        layout.addWidget(dropdownInput)
        layout.addWidget(QPushButton("X", clicked=lambda: self._deleteRow(row)))
        log.debug(f"Added {dropdownInput.objectName()}")

    def _deleteRow(self, row):  # can this ever be connected here rather than in the controller?
        self.layout.removeWidget(row)
        row.deleteLater()
        self.adjustSize()
        log.debug(f"Deleted row")

