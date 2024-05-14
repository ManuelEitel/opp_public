from PyQt5.QtWidgets import QWidget, QHeaderView, QApplication
from PyQt5.uic import (loadUi)
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtCore, Qt
from PyQt5.QtCore import Qt


class DistributeOverView(QWidget):

    distribute_cell_clicked = QtCore.pyqtSignal(int, int)
    employees_tw_clicked = QtCore.pyqtSignal(int, int)

    #  dist_by_hand_clicked = QtCore.pyqtSignal(int)  # comes later, when I need to manually give user tasks

    def __init__(self):
        """ bunch of buttons """
        super(DistributeOverView, self).__init__()
        loadUi("view/ui_files/workflow_distribute_step_btn_window.ui", self)
        self.btn_close.clicked.connect(self.close_fct)
        self.setWindowModality(Qt.ApplicationModal)  # make it, so you have to interact with the widget first
        self._table_autofill_horizontally()  # makes tables pretty

        self.btn_close.setStyleSheet('background-color: rgb(244, 242, 255); font: 12pt "Segoe UI";')
        self.giveTask.setStyleSheet('background-color: rgb(244, 242, 255); font: 12pt "Segoe UI";')
        self.tw_tasks.cellClicked.connect(self.handle_tw_cell_clicked)
        self.tw_employees.cellClicked.connect(self.handle_tw_employees_clicked)

        #  self.btn_task_by_hand.clicked.connect(self.dist_by_hand)

    def dist_by_hand(self):
        self.dist_by_hand_clicked.emit(1)

    def handle_tw_employees_clicked(self, row, columns):
        self.employees_tw_clicked.emit(row, columns)

    def close_fct(self):
        self.close()

    def _table_autofill_horizontally(self):
        """
        Table will fit the screen horizontally
        """

        self.tw_tasks.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tw_tasks.resizeColumnsToContents()

        self.tw_employees.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tw_employees.resizeColumnsToContents()

        self.tw_tasks.horizontalHeader().setStretchLastSection(True)
        self.tw_tasks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_employees.horizontalHeader().setStretchLastSection(True)
        self.tw_employees.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def handle_tw_cell_clicked(self, row, column):
        self.distribute_cell_clicked.emit(row, column)



