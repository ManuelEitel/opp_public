from view_timetable.py_user_overview_selector import ViewUserOverviewSelector
from databases.datatase_handler import Database
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore

from control_timetable.control_timetable_mw import ControlTimetableMainWindow


class ControlUserOverviewSelector(object):

    def __init__(self, model):

        self.model = model
        self.view_timetable_main = ViewUserOverviewSelector(self.model)
        self.rowCount = 0
        self.user = None
        self.control_timetable_mw = None
        self._autofill_users_at_start()
        self.view_timetable_main.tw_users.cellClicked.connect(self.handle_cell_click_fct)
        self.view_timetable_main.giveTask.clicked.connect(self.open_ctr_tt_mw)
        self.view_timetable_main.show()

    def open_ctr_tt_mw(self):
        if self.view_timetable_main.giveTask.text() != "Check Calendar of ":
            self.control_timetable_mw = ControlTimetableMainWindow(self.model, self.user)

    def handle_cell_click_fct(self, row, column):
        self.user = self.view_timetable_main.tw_users.item(row, column).text()
        self.view_timetable_main.giveTask.setText(f'Check Calendar of {self.user}')

    def _autofill_users_at_start(self):
        db = Database('databases/db_main.db')
        db.connect()

        query = "SELECT * FROM table_users WHERE rights = 'User'"

        all_users = db.fetch_data(query)

        for element in all_users:
            self.rowCount += 1
            username = element[0]
            item = QTableWidgetItem(username)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.view_timetable_main.tw_users.setRowCount(self.rowCount)
            self.view_timetable_main.tw_users.setItem(self.rowCount-1, 0, item)

