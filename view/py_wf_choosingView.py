from PyQt5.uic import loadUi
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QHeaderView, QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from model.model_main import ModelMain


class WFChoosingView(QMainWindow):

    cell_clicked_wf_choosing = qtc.pyqtSignal(str)

    def __init__(self, model: ModelMain):
        """
        The gui for the workflow windows' new step popup window is being done here.
        """

        super().__init__()
        loadUi("view/ui_files/workflow_choosingView.ui", self)
        self.model = model
        self.rowCount = 0

        self.setWindowModality(Qt.ApplicationModal)  # make it, so you have to interact with the widget first
        self.tw_wf_choosing.setMouseTracking(True)  # Enable mouse tracking for the entire widget
        self.distributed_workflow = None
        self.tw_wf_choosing.cellClicked.connect(self.handle_cell_click_fct)
        self.tw_wf_choosing.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tw_wf_choosing.resizeColumnsToContents()
        self._table_autofill_horizontally()
        self._name()
        self.table_list = []

    def handle_cell_click_fct(self, row, column):
        self.distributed_workflow = self.tw_wf_choosing.item(row, column).text()
        self.cell_clicked_wf_choosing.emit(self.distributed_workflow)
        print(f'got here at emitting')

    def _table_autofill_horizontally(self):
        """
        Table will fit the screen horizontally
        """
        self.tw_wf_choosing.horizontalHeader().setStretchLastSection(True)
        self.tw_wf_choosing.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _name(self):
        self.label_user_type_workflow_choosing.setText(self.model.current_rights)

