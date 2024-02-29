from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHeaderView

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from model.model_main import ModelMain


class DeleteWFStep(QWidget):

    deletion_clicked = qtc.pyqtSignal(int)

    def __init__(self, model: ModelMain, element_list: list):
        """
        The gui for the workflow windows' new step popup window is being done here.
        """

        super().__init__()
        self.model = model
        self.element_list = element_list

        loadUi("view/ui_files/workflow_deletestep.ui", self)
        self.setWindowModality(Qt.ApplicationModal)  # make it, so you have to interact with the widget first

        self.deletion_wf_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.deletion_wf_table.resizeColumnsToContents()
        self._table_autofill_horizontally()
        self._name()
        self.rowCount = 0
        self.btn_delete_step_wf.clicked.connect(self.deletion_clicked_fct)
        self._fill_workflow_deleteView()

    def _table_autofill_horizontally(self):
        """
        Table will fit the screen horizontally
        """
        self.deletion_wf_table.horizontalHeader().setStretchLastSection(True)
        self.deletion_wf_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _name(self):
        self.delete_wf_usertype.setText(self.model.current_rights)

    def deletion_clicked_fct(self):
        number = self.delete_spinBox.value()
        if number <= self.deletion_wf_table.rowCount():
            self.deletion_clicked.emit(number)
            self.close()
        elif number > self.deletion_wf_table.rowCount():
            self.delete_wf_feedback_label.setText("Step doesn't exist.")

    def _fill_workflow_deleteView(self):
        """
        If Steps are created already, the table in this window in now being filled.
        """
        if self.element_list:
            for element in self.element_list:
                i = 0
                self.rowCount += 1
                self.deletion_wf_table.setRowCount(self.rowCount)
                for entry in element[0:2]:
                    print(f'entry = {entry}')
                    item = QTableWidgetItem(entry)
                    self.deletion_wf_table.setItem(self.rowCount-1, i, item)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    i += 1

