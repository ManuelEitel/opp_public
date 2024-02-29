from view.py_wf_choosingView import WFChoosingView
from databases.datatase_handler import Database
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore
from PyQt5 import Qt


class PutWorkflowOnOrder(object):

    def __init__(self, model):
        print(f'got here 2')
        self.model = model
        self.wf_choosingView = WFChoosingView(self.model)
        self.wf_choosingView.show()
        print(f'got here')
        self._fill_workflow_table()

    def _fill_workflow_table(self):

        db = Database("databases/db_workflows.db")
        db.connect()

        select_tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = db.fetch_data(select_tables_query)
        db.close()

        for entry in tables:
            i = 0
            self.wf_choosingView.rowCount += 1
            self.wf_choosingView.tw_wf_choosing.setRowCount(self.wf_choosingView.rowCount)
            for element in entry:
                item = QTableWidgetItem(element)
                self.wf_choosingView.tw_wf_choosing.setItem(self.wf_choosingView.rowCount-1, i, item)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                i += 1
        self.wf_choosingView.table_list = tables
