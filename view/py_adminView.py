from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QWidget, QMainWindow, QApplication

from PyQt5.QtCore import Qt
from PyQt5 import QtCore as qtc


class AdminView(QMainWindow):

    admin_cell_clicked = qtc.pyqtSignal(int, int, Qt.MouseButton)
    make_user = qtc.pyqtSignal(int)

    def __init__(self):
        """
        This is the Delete Dialog View of the small Window, that the Operator can call to delete elements. \n
        Deletion will end in deprecation status change from 0 to 1.
        """

        super().__init__()
        loadUi("view/ui_files/admin_window.ui", self)
        self.setWindowModality(Qt.ApplicationModal)
        # self._bind()
        self.user_tableWidget.setMouseTracking(True)  # Enable mouse tracking for the entire widget

        self.user_tableWidget.cellClicked.connect(self.handle_cell_click)
        self.newUser.clicked.connect(self.create_user_pressed)
        self.deleteUser.clicked.connect(self.set_btn_status)

    def set_btn_status(self):
        # ToDo: There's a bug here, that the emit signal create user is being emitted twice.
        if self.deleteUser.isChecked():
            print(f'self checked is checked')
            self.deleteUser.setChecked(True)
        else:
            self.deleteUser.setChecked(False)

    def create_user_pressed(self):
        if self.deleteUser.isChecked():
            self.deleteUser.setChecked(False)
            self.newUser.clicked.connect(self.emit_signal_create_user_pressed)
            return
        elif not self.deleteUser.isChecked():
            self.newUser.clicked.connect(self.emit_signal_create_user_pressed)
            return

    def emit_signal_create_user_pressed(self):
        self.make_user.emit(1)

    def handle_cell_click(self, row, column):
        if self.deleteUser.isChecked():
            self.deleteUser.setChecked(False)
            mouse_button = QApplication.mouseButtons()
            self.admin_cell_clicked.emit(row, column, mouse_button)

        if not self.deleteUser.isChecked():
            self.deleteUser.setChecked(False)
