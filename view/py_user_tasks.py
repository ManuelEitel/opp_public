from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView, QMainWindow
from model.model_main import ModelMain
from PyQt5 import QtCore as qtc


class UserTasksView(QMainWindow):

    cell_clicked_user = qtc.pyqtSignal(int, int)
    next_week_clicked = qtc.pyqtSignal(int)
    prior_week_clicked = qtc.pyqtSignal(int)

    def __init__(self, model: ModelMain):
        """
        The gui for the workflow windows' new step popup window is being done here.
        """

        super().__init__()
        loadUi("view/ui_files/User_task_window.ui", self)
        self.setWindowTitle("UserTasksView")
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableWidget.cellClicked.connect(self.handle_cell_click)
        self._bind()

    def handle_cell_click(self, row, column):
        self.cell_clicked_user.emit(row, column)

    def _bind(self):
        self.btn_prior_week.clicked.connect(self.emit_prior_week)
        self.btn_next_week.clicked.connect(self.emit_next_week)

    def emit_next_week(self):
        """Positive Integer emitted (1) for next week"""
        self.next_week_clicked.emit(1)

    def emit_prior_week(self):
        """Negative Integer (-1) emitted for prior week"""
        self.prior_week_clicked.emit(-1)
