from PySide6.QtWidgets import QApplication
import sys
from lib.controller import Controller
from view.mainwindow import WSMain
from model.webservices import Webservices
from model.transactionstore import TransactionStore

app = QApplication(sys.argv)
mainWindow = WSMain()
api = Webservices()
model = TransactionStore()
controller = Controller(view=mainWindow, model=model, api=api)
sys.exit(app.exec())