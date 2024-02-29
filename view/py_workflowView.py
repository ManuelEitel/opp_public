from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QHeaderView
from PyQt5 import QtWidgets


class WorkflowWindowView(QMainWindow):

    def __init__(self):
        """
        The gui for the workflow window is being done here.
        """
        super().__init__()

        loadUi("view/ui_files/workflowView_2.ui", self)

        self.tableWidget_Workflow.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_Workflow.resizeColumnsToContents()
        self._table_autofill_horizontally()

    def _table_autofill_horizontally(self):
        """
        Table will fit the screen horizontally
        """
        self.tableWidget_Workflow.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_Workflow.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
