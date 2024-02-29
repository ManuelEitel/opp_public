from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QPushButton, QTableWidgetItem, QTableWidget, QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt


class MainWindowView(QMainWindow):

    change_style = qtc.pyqtSignal(QPushButton, QPushButton, QPushButton, str)
    cell_clicked = qtc.pyqtSignal(int, int, Qt.MouseButton)
    mode_btn_clicked_del_wf = qtc.pyqtSignal(int)

    def __init__(self):

        super().__init__()
        loadUi("view/ui_files/mainWindow_asMainWindow.ui", self)

        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.resizeColumnsToContents()

        self.button_color_type_short = "background-color :rgb(0, 157, 205);font-size:10pt;"
        self.button_color_type_long = "background-color:rgb(0, 157, 255);color:rgb(212, 255, 70);font-size:10pt;"

        self._table_autofill_horizontally()
        self._make_mode_buttons_toggle_buttons()
        self._bind_mode_buttons()

        self.tableWidget.setMouseTracking(True)  # Enable mouse tracking for the entire widget

        self.tableWidget.cellClicked.connect(self.handle_cell_click)

    def update_btns_all(self):
        self.deleteOrder.setChecked(False)
        self.changeOrder.setChecked(False)
        self.distributeTask.setChecked(False)
        self.deleteOrder.setStyleSheet(self.button_color_type_long)
        self.changeOrder.setStyleSheet(self.button_color_type_long)
        self.distributeTask.setStyleSheet(self.button_color_type_long)

    def change_button_style(self, mode_name: str):
        """Make the designs according to pressed button type - only ui-change"""

        if mode_name == "delete":
            if self.deleteOrder.isChecked():
                self.deleteOrder.setStyleSheet(self.button_color_type_short)
                self.changeOrder.setChecked(False)
                self.distributeTask.setChecked(False)
                self.changeOrder.setStyleSheet(self.button_color_type_long)
                self.distributeTask.setStyleSheet(self.button_color_type_long)
            else:
                self.deleteOrder.setStyleSheet(self.button_color_type_long)

        if mode_name == "change":
            if self.changeOrder.isChecked():
                self.changeOrder.setStyleSheet(self.button_color_type_short)
                self.deleteOrder.setChecked(False)
                self.distributeTask.setChecked(False)
                self.deleteOrder.setStyleSheet(self.button_color_type_long)
                self.distributeTask.setStyleSheet(self.button_color_type_long)
            else:
                self.changeOrder.setStyleSheet(self.button_color_type_long)

        if mode_name == "distribute":
            if self.distributeTask.isChecked():
                self.distributeTask.setStyleSheet(self.button_color_type_short)
                self.deleteOrder.setChecked(False)
                self.changeOrder.setChecked(False)
                self.deleteOrder.setStyleSheet(self.button_color_type_long)
                self.changeOrder.setStyleSheet(self.button_color_type_long)
            else:
                self.distributeTask.setStyleSheet(self.button_color_type_long)

    def handle_cell_click(self, row, column):
        mouse_button = QApplication.mouseButtons()
        self.cell_clicked.emit(row, column, mouse_button)

    def _make_mode_buttons_toggle_buttons(self):
        """
        Make the three mode buttons from operator toggle- able
        """
        self.deleteOrder.setCheckable(True)
        self.changeOrder.setCheckable(True)
        self.distributeTask.setCheckable(True)

    def _bind_mode_buttons(self):
        """
        Bind the buttons to function self.on_mode_x for ui change of the buttons and signal to upper class
        """
        self.deleteOrder.clicked.connect(lambda: self.on_mode_x("delete"))
        self.changeOrder.clicked.connect(lambda: self.on_mode_x("change"))
        self.distributeTask.clicked.connect(lambda: self.on_mode_x("distribute"))

    def _table_autofill_horizontally(self):
        """
        Table will fit the screen horizontally
        """
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def on_mode_x(self, mode_name: str):
        """
        modes are
        view, delete, change, distribute
        """
        self.change_button_style(mode_name)

        self.mode_btn_clicked_del_wf.emit(1)

        if mode_name == "delete":
            self.change_style.emit(self.deleteOrder, self.changeOrder, self.distributeTask, mode_name)
        elif mode_name == "change":
            self.change_style.emit(self.deleteOrder, self.changeOrder, self.distributeTask, mode_name)
        elif mode_name == "distribute":
            self.change_style.emit(self.deleteOrder, self.changeOrder, self.distributeTask, mode_name)

    def change_mode_styles(self, buttons: dict, mode: str, change_needed_var: bool):
        """
        POTENTIONALLY DELETEABLE
        Not Static (90%)
        Takes the buttons and puts them into the mode color scheme such, that all, but mode is normal \n
        mode - button becomes yellow \n
                self.buttons = {"New Order": self.mainWindowView.newOrder, \n
                        "Delete Order": self.mainWindowView.deleteOrder, \n
                        "Change Order": self.mainWindowView.changeOrder, \n
                        "Distribute Task": self.mainWindowView.distributeTask, \n
                        "Standard Order 1": self.mainWindowView.standardOrder1, \n
                        "Standard Order 2": self.mainWindowView.standardOrder2, \n
                        "Create Workflow": self.mainWindowView.createWorkflow} \n
        """
        if change_needed_var:
            try:
                for element in buttons.values():
                    element.setStyleSheet("background-color:rgb(0, 157, 255);color:rgb(212, 255, 70);font-size:10pt;")
            except AttributeError as e:
                print(f'AttributeError {e}')

            buttons[mode].setStyleSheet("background-color : yellow")
        else:
            try:
                for element in buttons.values():
                    element.setStyleSheet("background-color:rgb(0, 157, 255);color:rgb(212, 255, 70);font-size:10pt;")
            except AttributeError as e:
                print(f'AttributeError {e}')

