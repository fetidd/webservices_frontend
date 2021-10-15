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
        log.debug(f"Creating a new {requestType.name} window")

        self.setWindowTitle(f"New {requestType.name}")
        self.requestType = requestType
        self.transactions = transactions
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.rows = []
        self.fields = [field for field, data in cfg.FIELDS.items() if data["inc"] & self.requestType.value]

        # Set up requestWindow based on requestType
        self.layout.addWidget(QLabel(cfg.INSTRUCTIONS[requestType]))
        if requestType == RequestType.TRANSACTIONQUERY:
            self._addDatePicker()
        elif requestType == RequestType.REFUND and len(self.transactions) > 0:
            self._addBatchRefundComponents()
        elif requestType in [
            RequestType.AUTH,
            RequestType.REFUND,
            RequestType.ACCOUNTCHECK,
        ]:
            self._addRequiredFields()

        self.buttonRow = QHBoxLayout()
        self.layout.addLayout(self.buttonRow)

        if (not (requestType == RequestType.REFUND and len(self.transactions))) and (not requestType == RequestType.ACCOUNTCHECK) > 0:
            self._addNewFieldButton()
        self._addSubmitButton()
        if requestType == RequestType.CUSTOM:
            for i in range(6):
                self._addDropdownRow(self.fields)

    def _addDatePicker(self):
        row = QWidget()
        rowLayout = QHBoxLayout()
        row.setLayout(rowLayout)
        self.startInput = QCalendarWidget()
        self.endInput = QCalendarWidget()
        rowLayout.addWidget(self.startInput)
        rowLayout.addWidget(self.endInput)
        self.layout.addWidget(row)

    def _addNewFieldButton(self):
        newFieldButton = QPushButton("New field", clicked=lambda: self._addDropdownRow(self.fields))
        newFieldButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.buttonRow.addWidget(newFieldButton)

    def _addSubmitButton(self):
        self.submitButton = QPushButton("Submit request")
        self.submitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.buttonRow.addWidget(self.submitButton)

    def _addRequiredFields(self):
        self.requiredInputs = {}
        for field, data in cfg.FIELDS.items():
            if data["req"] & self.requestType.value:
                row = QHBoxLayout()
                fieldInput = QLineEdit()
                self.requiredInputs[field] = fieldInput
                row.addWidget(QLabel(field))
                row.addWidget(fieldInput)
                self.layout.addLayout(row)

    def _addBatchRefundComponents(self):
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




