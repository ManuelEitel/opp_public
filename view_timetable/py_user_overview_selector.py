from PyQt5.QtWidgets import QWidget, QHeaderView
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets



class ViewUserOverviewSelector(QWidget):
    def __init__(self, model):

        super().__init__()

        self.model = model
        loadUi("view_timetable/ui_files_timetable/user_overview_selector.ui", self)
        self._name()
        self._table_autofill_horizontally()
        self._bind()

    def _bind(self):
        self.btn_close.clicked.connect(self.close)



    def _table_autofill_horizontally(self):
        """
        Table will fit the screen horizontally
        """

        self.tw_users.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tw_users.resizeColumnsToContents()

        self.tw_users.horizontalHeader().setStretchLastSection(True)
        self.tw_users.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _name(self):
        self.usertype_label.setText(self.model.current_rights)
