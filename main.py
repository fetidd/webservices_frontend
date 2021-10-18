from PySide6.QtWidgets import QApplication
import sys, os, pickle

from lib.config import Config
from lib.controller import Controller
from view.mainwindow import WSMain
from model.webservices import Webservices
from model.transactionstore import TransactionStore

app = QApplication(sys.argv)
settingsPath = "./settings.pkl"
if os.path.exists(settingsPath):
    config = pickle.load(open(settingsPath, "rb"))
else:
    config = Config()
mainWindow = WSMain(config)
api = Webservices()
model = TransactionStore()
controller = Controller(view=mainWindow, model=model, api=api, config=config)
sys.exit(app.exec())
